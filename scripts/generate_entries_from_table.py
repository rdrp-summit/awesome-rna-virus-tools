import csv
import json
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# Helper functions for external metadata lookup
# ----------------------------------------------------------------------
def fetch_crossref_metadata(doi: str) -> dict:
    """Retrieve Crossref metadata (date, title, URL) for a given DOI."""
    api_url = f"https://api.crossref.org/works/{doi}"
    try:
        resp = requests.get(api_url, timeout=10)
        if resp.status_code != 200:
            return {}
        data = resp.json().get("message", {})
        # Extract publication year/month/day if available
        date_parts = (data.get("published-print") or data.get("published-online") or {}).get("date-parts", [[None]])[0]
        date_str = None
        if date_parts and date_parts[0]:
            # Build YYYY-MM-DD, filling missing month/day with 01
            year = str(date_parts[0])
            month = f"{date_parts[1]:02d}" if len(date_parts) > 1 else "01"
            day = f"{date_parts[2]:02d}" if len(date_parts) > 2 else "01"
            date_str = f"{year}-{month}-{day}"
        return {
            "date": date_str,
            "title": data.get("title", [None])[0],
            "url": data.get("URL")
        }
    except Exception:
        return {}

def fetch_entrez_pmid(pmid: str) -> dict:
    """Fetch PubMed metadata (date, title, DOI) using NCBI Entrez utilities."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "pubmed", "id": pmid, "retmode": "json"}
    try:
        resp = requests.get(base, params=params, timeout=10)
        if resp.status_code != 200:
            return {}
        result = resp.json()
        record = result.get("result", {}).get(pmid, {})
        # Convert PubDate like "2024 Jul 29" to ISO format
        pubdate = record.get("pubdate", "")
        iso_date = None
        if pubdate:
            try:
                parts = pubdate.split()
                year = parts[0]
                month_map = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                             "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                             "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
                month = month_map.get(parts[1][:3], "01") if len(parts) > 1 else "01"
                day = parts[2] if len(parts) > 2 else "01"
                iso_date = f"{year}-{month}-{day.zfill(2)}"
            except Exception:
                pass
        return {
            "date": iso_date,
            "title": record.get("title"),
            "doi": record.get("elocationid")
        }
    except Exception:
        return {}

def slugify(text: str) -> str:
    """Convert a title into a safe filename slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text

# ----------------------------------------------------------------------
# Main generation logic
# ----------------------------------------------------------------------
def main():
    csv_path = Path(__file__).resolve().parents[0] / ".." / "entries" / "from_gdrive.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    output_dir = Path(__file__).resolve().parents[0] / ".." / "entries"
    output_dir.mkdir(parents=True, exist_ok=True)

    fieldnames = ["date", "title", "topics", "pmid", "link"]
    created = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        # Skip header row
        next(reader, None)

        for row in reader:
            title = row["title"].strip()
            if not title:
                continue

            entry = {
                "name": title,
                "url": row["link"].strip() or None,
                "doi": None,
                "bibtex": None,
                "description": "",
                "date": row["date"].strip() or None,
                "version": None,
                "license": None,
                "language": None,
                "package_managers": None,
                "package_manager": None,
                "installation_methods": None,
                "platforms": None,
                "input_formats": None,
                "output_formats": None,
                "topics": [],
                "pmid": row["pmid"].strip() or None,
                "type": "paper",
                "interface": "CLI"
            }

            # ------------------------------------------------------------------
            # Topics – preserve exactly as supplied, no new keywords added
            # ------------------------------------------------------------------
            raw_topics = row["topics"].strip()
            if raw_topics:
                entry["topics"] = [t.strip() for t in raw_topics.split(",") if t.strip()]
            else:
                entry["topics"] = ["virus discovery", "rna virus"]

            # ------------------------------------------------------------------
            # Resolve DOI from URL if possible
            # ------------------------------------------------------------------
            doi_candidate = None
            if entry["url"] and "doi.org" in entry["url"]:
                doi_candidate = entry["url"].split("doi.org/")[-1]
                entry["doi"] = doi_candidate

            # ------------------------------------------------------------------
            # If we have a DOI, fetch additional metadata via Crossref
            # ------------------------------------------------------------------
            if doi_candidate:
                meta = fetch_crossref_metadata(doi_candidate)
                if meta:
                    entry["doi"] = doi_candidate
                    entry["url"] = meta.get("url") or entry["url"]
                    if not entry["date"] and meta.get("date"):
                        entry["date"] = meta["date"]
                    if not entry["description"] and meta.get("title"):
                        entry["description"] = meta["title"]

            # ------------------------------------------------------------------
            # If PMID is present, enrich via Entrez
            # ------------------------------------------------------------------
            if entry["pmid"]:
                entrez = fetch_entrez_pmid(entry["pmid"])
                if entrez:
                    if not entry["date"] and entrez.get("date"):
                        entry["date"] = entrez["date"]
                    if not entry["doi"] and entrez.get("doi"):
                        entry["doi"] = entrez["doi"]
                    if not entry["description"] and entrez.get("title"):
                        entry["description"] = entrez["title"]

            # ------------------------------------------------------------------
            # Infer entry type & interface heuristically from title
            # ------------------------------------------------------------------
            lowered = title.lower()
            if any(tok in lowered for tok in ["tool", "pipeline", "software", "method"]):
                entry["type"] = "tool"
            elif any(tok in lowered for tok in ["database", "catalog", "repository"]):
                entry["type"] = "database"

            if any(tok in lowered for tok in ["cli", "command line"]):
                entry["interface"] = "CLI"
            elif any(tok in lowered for tok in ["tui", "terminal ui"]):
                entry["interface"] = "TUI"
            elif any(tok in lowered for tok in ["gui", "graphical"]):
                entry["interface"] = "gui"
            elif "nextflow" in lowered:
                entry["interface"] = "nextflow"
            elif "snakemake" in lowered:
                entry["interface"] = "snakemake"

            # ------------------------------------------------------------------
            # Write JSON file
            # ------------------------------------------------------------------
            filename = f"{slugify(title)}.json"
            path = output_dir / filename
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)
            created += 1

    print(f"Generated {created} entry files in {output_dir}")

if __name__ == "__main__":
    main()