import json
import re
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
import polars as pl
import jsonschema
from glob import glob
# # External data fetch helpers
# ENTREZ_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
# ENTREZ_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
# EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
CROSSREF_API = "https://api.crossref.org/works"

rna_tool_polars_schema = {
    # Name of the tool (Slug for the entry)
    "name": pl.Utf8,

    # paper title or tool one-liner
    "title": pl.Utf8,                     # ["string", "null"]

    # URL to the tool's homepage or repository
    "url": pl.Utf8,                     # format: uri

    # DOI of the associated publication
    "doi": pl.Utf8,                     # ["string", "null"]

    # BibTeX citation for the tool
    "bibtex": pl.Utf8,                  # ["string", "null"]

    # Brief description of what the tool does
    "description": pl.Utf8,

    # Publication or release date (YYYY‑MM‑DD format)
    "date": pl.Date,                    # ["string", "null"], format: date

    # Latest version of the tool
    "version": pl.Utf8,                 # ["string", "null"]

    # Software license
    "license": pl.Utf8,                 # ["string", "null"]

    # Primary programming language
    "language": pl.Utf8,                # ["string", "null"]

    # Package managers through which the tool can be installed
    # enum: ['pip', 'conda', 'bioconda', 'npm', 'cran', 'cpan', 'gem',
    #        'cargo', 'go', 'homebrew', 'apt', 'yum', 'docker',
    #        'singularity', 'github', 'source', 'null']
    "package_managers": pl.List(pl.Utf8),   # ["array", "null"]

    # Supported input file formats (e.g., FASTA, FASTQ, SAM, BAM)
    "input_formats": pl.List(pl.Utf8),      # ["array", "null"]

    # Generated output file formats
    "output_formats": pl.List(pl.Utf8),     # ["array", "null"]

    # List of topics/categories this tool belongs to
    "topics": pl.List(pl.Utf8),              # ["array", "null"]

    # Category of the entry
    # enum: ['tool', 'database', 'paper']
    "type": pl.Utf8,

    # Primary interface type
    # enum: ['CLI', 'TUI', 'gui', 'nextflow', 'snakemake', 'null']
    "interface": pl.List(pl.Utf8),                # ["array", "null"]
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def doi_to_bibtex_crossref(doi: str) -> dict:
    """Retrieve Crossref metadata (date, title, URL) for a DOI."""
    headers = {"Accept": "applicatio    n/x-bibtex"}
    url = f"{CROSSREF_API}/{doi}/transform/application/x-bibtex"
    resp = requests.get(f"{url}", headers=headers, timeout=10)
    if resp.status_code != 200:
        return None
    return BeautifulSoup(resp.text.strip()).get_text()

def fetch_crossref_metadata(doi: str) -> dict:
    """Retrieve Crossref metadata (date, title, URL) for a DOI."""
    try:
        resp = requests.get(f"{CROSSREF_API}/{doi}", timeout=10)
        if resp.status_code != 200:
            return {}
        msg = resp.json().get("message", {})

        # inconsistency in the date format – for missing day use first of the month
        date_parts = (msg.get("published-print") or msg.get("published-online") or {}).get(
            "date-parts", [[None]]
        )[0]
        date_str = None
        if date_parts and date_parts[0]:
            year = str(date_parts[0])
            month = f"{date_parts[1]:02d}" if len(date_parts) > 1 else "01"
            day = f"{date_parts[2]:02d}" if len(date_parts) > 2 else "01"
            date_str = f"{year}-{month}-{day}"
        return {
            "date": date_str,
            "title": msg.get("title", [None])[0],
            # "license": msg.get("license", None),
            "abstract": msg.get("abstract", None),
        }
    except:
        return  pl.Struct(fields={"date": pl.String, "title": pl.String, 
                                #   "license":pl.String,
                                  "abstract":pl.String })

# def strip_http(doi: str) -> str | None:
#     """Strip URL prefix and ensure a valid DOI."""
#     if doi and isinstance(doi, str):
#         # NOTE: the original code used `spli`; replace with `replace`
#         doi = doi.replace("doi.org/", "")
#         if doi.startswith("10."):
#             return doi
#     return None

def doi_to_url(url: str | None, doi: str | None) -> str | None:
    """Return the URL if valid, otherwise fallback to DOI URL or None."""
    if url and isinstance(url, str) and url.startswith(("http://", "https://", "ftp://")):
        return url
    if doi:
        return f"https://doi.org/{doi}"
    return None

def slugify(text: str) -> str:
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def validate_entry(entry_path: Path, schema: Dict[str, Any]) -> List[str]:
    """Validate a single entry against the schema."""
    errors = []
    try:
        with entry_path.open("r") as f:
            entry_data = json.load(f)

        # Validate against schema
        try:
            jsonschema.validate(entry_data, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message} in {entry_path.name}")
            logger.error(f"Error in {entry_path.name}: {e}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")

        # Additional custom validations
        errors.extend(validate_custom_rules(entry_data))

    except Exception as e:
        logger.error(f"An error occurred while validating {entry_path.name}: {e}")
    return errors


def validate_custom_rules(entry: Dict[str, Any]) -> List[str]:
    """Apply custom validation rules beyond the schema."""
    errors = []
    warnings =[]

    # Check URL accessibility (basic format check)
    url = entry.get('url', '')
    if url is not None and not (url.startswith('http://') or url.startswith('https://')):
        errors.append("URL should start with http:// or https://")

    # Check DOI format
    doi = entry.get('doi', '')
    if doi and not doi.startswith('10.'):
        errors.append("DOI should start with '10.'")

    # Check date format
    date = entry.get('date', '')
    if date:
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            errors.append("Date should be in YYYY-MM-DD format")

    # Check topics are not empty
    topics = entry.get('topics', [])
    if not topics:
        errors.append("At least one topic is required")

    # Description length checks
    description = entry.get('description', '')
    if description is not None and len(description) > 1200:
        warnings.append("Description is very long (>1200 chars), consider shortening")
    if description is not None and len(description) < 10:
        errors.append("Description is very short (<10 chars), consider expanding")

    return errors


def validate_all_entries(entries_dir: str, schema_path: str) -> bool:
    """Validate all entries and return True if all are valid."""
    entries_path = Path(entries_dir)

    if not entries_path.exists():
        logger.error(f"Entries directory not found: {entries_dir}")
        return False

    # Load schema
    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load schema: {e}")
        return False

    json_files = list(entries_path.glob("*.json"))
    if not json_files:
        logger.warning(f"No JSON files found in {entries_dir}")
        return True

    logger.info(f"Validating {len(json_files)} entries...")

    all_valid = True
    total_errors = 0
    total_warnings = 0

    for json_file in sorted(json_files):
        errors = validate_entry(json_file, schema)

        if errors:
            all_valid = False
            logger.error(f"\n❌ {json_file.name}:")
            for err in errors:
                if err.startswith("Warning:"):
                    logger.warning(f"  {err}")
                    total_warnings += 1
                else:
                    logger.error(f"  {err}")
                    total_errors += 1
        else:
            logger.info(f"✅ {json_file.name}")

    # Summary
    logger.info("\n📊 Validation Summary:")
    logger.info(f"  Total files: {len(json_files)}")
    logger.info(f"  Valid files: {len(json_files) - total_errors}")
    logger.info(f"  Total errors: {total_errors}")
    logger.info(f"  Total warnings: {total_warnings}")

    if all_valid:
        logger.info("🎉 All entries are valid!")
    else:
        logger.error("❌ Some entries have validation errors")

    return all_valid

def main() -> None:
    parser = argparse.ArgumentParser(description="Entry processor")
    parser.add_argument(
        "--entries-dir",
        default="entries",
        help="Directory containing entry JSON files",
    )
    parser.add_argument(
        "--schema",
        default="scripts/schema.json",
        help="Path to JSON schema file",
    )
    parser.add_argument(
        "--parquet",
        default="entries/from_gdrive.parquet",
        help="Path to parquet  containing entries",
    )
    args = parser.parse_args()

    # Load schema
    # schema = json.load(open(args.schema, "r"))
    # schema_df = pl.DataFrame(schema=rna_tool_polars_schema) # prefer to use relaxed join for cohersion
    # df_list = [pl.read_json(str(p)) for p in Path(args.entries_dir).glob("*.json")]
    # dfs = pl.concat(df_list,how="diagonal_relaxed")
    # dfs = pl.concat([dfs,schema_df],how="diagonal_relaxed")
    # tsv_df = pl.read_parquet(args.parquet,separator="\t")
    # listcols = schema_df.select(pl.selectors.by_dtype(pl.List(pl.Utf8))).columns
    # tsv_df = tsv_df.with_columns(pl.selectors.by_name(listcols).str.replace_all(", ",",").str.split(by=","))

    # entries_df =  pl.concat([dfs,tsv_df],how="diagonal_relaxed")
    # logger.info(f"Processing {entries_df.height} rows from {args.parquet}")

    # entries_df = entries_df.with_columns(
    #     pl.col("doi").map_elements(doi_to_bibtex_crossref,return_dtype= pl.String).alias("bibtex")
    # )
    # # there is probably a way to get the bibtex from the full metadata, but I am lazy
    # entries_df = entries_df.with_columns(
    #     pl.col("doi").map_elements(fetch_crossref_metadata,return_dtype= pl.Struct(fields={"date": pl.String, "title": pl.String,"abstract":pl.String })).alias("tmpy")
    # )

    # entries_df=entries_df.unique()

    # entries_df = entries_df.with_columns(
    #     # Title: prefer existing, otherwise use the title from Crossref
    #     pl.coalesce([
    #         pl.col("title"),
    #         pl.col("tmpy").struct.field("title")
    #     ]).alias("title"),

    #     # Date: prefer existing, otherwise use the date from Crossref
    #     pl.coalesce([
    #         pl.col("date"),
    #         pl.col("tmpy").struct.field("date")
    #     ]).alias("date"),

    #     # Description: prefer existing, otherwise use the abstract from Crossref  # TODO: need to think of a cleaner way to clean
    #     pl.coalesce([
    #         pl.col("description"),
    #         pl.col("tmpy").struct.field("abstract"),
    #         pl.col("tmpy").struct.field("title")
    #     ]).str.replace_all("<jats:p>","").str.replace_all("",literal=True,value="").str.replace_all("   <jats:p>","").str.replace_all(".</jats:p>",literal=True,value="").alias("description")
    # ).drop("tmpy")   # Temporary helper column no longer needed

    # # add url link from doi if missing
    # entries_df = entries_df.with_columns(
    #     pl.when(pl.col("url").is_null())
    #     .then(
    #         # Concatenate the DOI prefix with the DOI value
    #         pl.concat_str([pl.lit("https://doi.org/"), pl.col("doi")])
    #     )
    #     .otherwise(pl.col("url"))          # keep the original URL when present
    #     .alias("url")
    # )

    # # add name (slug) if none
    # entries_df = entries_df.with_columns(
    #     pl.concat_str([pl.col("title").str.head(80).map_elements(slugify,return_dtype=pl.String),pl.col("date").str.head(4)],separator="_")
    #     .alias("name")
    # )

    # # for i in range(entries_df.height):
    # #     entries_df[i].write_json(file=f"entries/{entries_df[i]['name'].to_list()[0]}.json")
    # for row in entries_df.iter_rows(named=True):
    #     (Path("entries") / f"{row['name']}.json").write_text(
    #         json.dumps(row, ensure_ascii=False, indent=2) + "\n",
    #         encoding="utf-8",
    #     )

    test = validate_all_entries(entries_dir=args.entries_dir,schema_path=args.schema)



if __name__ == "__main__":
    main()