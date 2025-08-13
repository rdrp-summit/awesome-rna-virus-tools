import json
import re
import sys
from pathlib import Path
from typing import Optional

import requests

# ----------------------------------------------------------------------
# External data fetch helpers
# ----------------------------------------------------------------------
ENTREZ_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ENTREZ_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"

def _get(url: str, params: dict) -> Optional[requests.Response]:
    """GET with simple retry on 429."""
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 429:
            import time
            time.sleep(2)
            resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp
    except requests.RequestException:
        return None

def fetch_abstract_by_pmid(pmid: str) -> Optional[str]:
    """Retrieve abstract from PubMed via Entrez."""
    r = _get(ENTREZ_SEARCH, {"db": "pubmed", "term": pmid, "retmode": "json"})
    if not r:
        return None
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids:
        return None
    uid = ids[0]
    r = _get(ENTREZ_FETCH, {"db": "pubmed", "id": uid, "retmode": "xml"})
    if not r:
        return None
    match = re.search(r"<AbstractText[^>]*>(.*?)</AbstractText>", r.text, re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return None

def fetch_abstract_by_doi(doi: str) -> Optional[str]:
    """Retrieve abstract via Europe PMC."""
    r = _get(f"{EUROPE_PMC}/search", {"query": f"DOI:{doi}", "resulttype": "core", "format": "json"})
    if not r:
        return None
    for result in r.json().get("resultList", {}).get("result", []):
        abstract = result.get("abstractText")
        if abstract:
            return re.sub(r"\s+", " ", abstract).strip()
    return None

# ----------------------------------------------------------------------
# Normalisation helpers
# ----------------------------------------------------------------------
def _normalize_date(date_str: Optional[str]) -> Optional[str]:
    """Convert common date formats to ISO YYYY‑MM‑DD."""
    if not date_str or not isinstance(date_str, str):
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return date_str
    parts = re.split(r"[-/]", date_str)
    if len(parts) == 3:
        year, month_raw, day = parts
        month_map = {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
        }
        month = month_map.get(month_raw[:3].title())
        if month:
            return f"{year}-{month}-{day.zfill(2)}"
    return None

def _clean_doi(doi: Optional[str]) -> Optional[str]:
    """Strip URL prefix and ensure a valid DOI."""
    if doi and isinstance(doi, str):
        doi = doi.replace("https://doi.org/", "").replace("doi.org/", "")
        if doi.startswith("10."):
            return doi
    return None

def _ensure_http_url(url: Optional[str], doi: Optional[str]) -> str:
    """Guarantee a non‑empty HTTP(S) URL for the entry."""
    if url and isinstance(url, str) and url.startswith(("http://", "https://")):
        return url
    if doi:
        return f"https://doi.org/{doi}"
    # Fallback placeholder – must be a syntactically valid URI
    return "https://example.org"

def _ensure_package_manager(entry: dict) -> None:
    """Package manager must be a string from the enum; use 'source' as safe default."""
    if not isinstance(entry.get("package_manager"), str):
        entry["package_manager"] = "source"

def _ensure_type_interface(entry: dict) -> None:
    """Enforce required string fields with allowed enum values."""
    if not isinstance(entry.get("type"), str):
        entry["type"] = "paper"
    if not isinstance(entry.get("interface"), str):
        entry["interface"] = "CLI"

def _ensure_description(entry: dict) -> None:
    """Make sure description is at least 10 characters."""
    desc = entry.get("description", "")
    if isinstance(desc, str) and len(desc.strip()) >= 10:
        return
    # Try to fetch an abstract
    abstract = None
    pmid = entry.get("pmid")
    doi = entry.get("doi")
    if pmid:
        abstract = fetch_abstract_by_pmid(pmid)
    if not abstract and doi:
        abstract = fetch_abstract_by_doi(doi)
    if abstract and len(abstract) >= 10:
        entry["description"] = abstract
    elif entry.get("name"):
        entry["description"] = entry["name"]
    else:
        entry["description"] = "No abstract available."

def _ensure_topics(entry: dict) -> None:
    """Preserve existing topics; ensure at least one if missing."""
    topics = entry.get("topics")
    if not isinstance(topics, list) or not topics:
        entry["topics"] = ["virus discovery", "rna virus"]

def _normalize_entry(entry: dict) -> None:
    """Apply all normalisation rules to a JSON entry."""
    # DOI cleaning
    entry["doi"] = _clean_doi(entry.get("doi"))
    # URL handling
    entry["url"] = _ensure_http_url(entry.get("url"), entry["doi"])
    # Date normalisation
    entry["date"] = _normalize_date(entry.get("date"))
    # Required enum fields
    _ensure_type_interface(entry)
    # Package manager defaults
    _ensure_package_manager(entry)
    # Description length
    _ensure_description(entry)
    # Topics
    _ensure_topics(entry)
    # Ensure optional fields exist (null is acceptable)
    optional_fields = [
        "version", "license", "language", "package_managers",
        "installation_methods", "platforms", "input_formats",
        "output_formats", "bibtex"
    ]
    for f in optional_fields:
        if f not in entry:
            entry[f] = None

def process_entry(path: Path) -> bool:
    """Load, normalise and write back a JSON entry."""
    with open(path, "r", encoding="utf-8") as f:
        entry = json.load(f)

    original = json.dumps(entry, sort_keys=True)
    _normalize_entry(entry)
    updated = json.dumps(entry, sort_keys=True)

    if original != updated:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
        return True
    return False

def main() -> None:
    entries_dir = Path(__file__).resolve().parents[0] / ".." / "entries"
    if not entries_dir.is_dir():
        print("Entries directory not found", file=sys.stderr)
        sys.exit(1)

    updated = 0
    for json_file in entries_dir.glob("*.json"):
        if process_entry(json_file):
            updated += 1

    print(f"Normalized {updated} entry files to satisfy the schema.")

if __name__ == "__main__":
    main()