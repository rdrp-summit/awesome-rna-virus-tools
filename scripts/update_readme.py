from datetime import datetime
# import json
# import textwrap
# import re
import logging
import argparse
from pathlib import Path
# import time

# from bs4 import BeautifulSoup
import polars as pl
# from glob import glob

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
    "date": pl.String,                    # ["string", "null"], format: date # edit - read as string, convert later (maybe)

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




def entry_2_md(entry: pl.DataFrame):
    """Take a row with the entry details and create markdown for it."""
    # Common fields
    title = entry["title"]
    url = entry["url"] if entry["url"] else ""
    description = entry["description"] if entry["description"] else ""
    topics = entry["topics"]
    first_topic = topics[0] if topics else "Misc"
    entry_type = entry["type"]

    # Build markdown based on type
    if entry_type == "paper":
        # Collapsible section for papers
        mk_str = f"""<details>
<summary>**{title}**</summary>

{description}

**DOI:** [{entry["doi"]}](https://doi.org/{entry["doi"]})
**URL:** {url}
**Topics:** {", ".join(topics)}
</details>

"""
    else:
        # Tools and databases as simple list items
        link = f"[{title}]({url})" if url else title
        mk_str = f"""- **{link}** ({", ".join(topics[1:])})
  {description}

"""
    return mk_str





# (Removed stray return; function now returns correctly above)
def add_nav_md(entries_df):
    """Generate a quick navigation markdown linking to type sections and topic subsections."""
    nav_lines = []
    # Define the order of sections
    type_order = [("tool", "Tools"), ("database", "Databases"), ("paper", "Papers")]
    for entry_type, display_name in type_order:
        type_entries = entries_df.filter(pl.col("type") == entry_type)
        if type_entries.height == 0:
            continue
        # Link to the type heading
        type_anchor = entry_type.lower()
        nav_lines.append(f"- [{display_name}](#{type_anchor})")
        # Gather unique first topics preserving order
        seen = set()
        for row in type_entries.iter_rows(named=True):
            topics = row.get("topics", [])
            first_topic = topics[0].title() if topics else "Misc"
            if first_topic in seen:
                continue
            seen.add(first_topic)
            topic_anchor = f"{entry_type}-{first_topic}".replace(" ", "-").lower()
            nav_lines.append(f"  - [{first_topic}](#{topic_anchor})")
        nav_lines.append("")  # blank line after each type
    return "\n".join(nav_lines)


def readme_header():
    mk_str = """
# Awesome RNA Virus Tools  
<img src="rdrp_summit.png" alt="drawing" width="200"/>  

> [!WARNING]  
THis repo is new and has bugs and errors, feel free to help out  

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Website](https://img.shields.io/website?url=https%3A//rdrp-summit.github.io/awesome-rna-virus-tools/)](https://rdrp-summit.github.io/awesome-rna-virus-tools/) [![GitHub](https://img.shields.io/github/license/rdrp-summit/awesome-rna-virus-tools)](LICENSE)
  
A curated list of software, tools, databases and resources for RNA virus analysis, prediction, annotation, phylogenetics, and related research. This project builds upon the excellent [awesome-virome](https://github.com/shandley/awesome-virome) list.

🌐 **[Visit the interactive website](https://rdrp-summit.github.io/awesome-rna-virus-tools/)** to explore tools by categories, programming languages, etc.
    """
    return mk_str


def readme_footer():
    """Generate the footer section of the README."""
    return """\n
## Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for details on how to add new tools or improve existing entries.

### How to Add a Tool

1. Create a new JSON file in the `entries/` directory
2. Follow the schema defined in `scripts/schema.json`
3. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [awesome-virome](https://github.com/shandley/awesome-virome) project
- Built with ❤️ by the RNA virus research community

---

*Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """*
    """




def main() -> None:
    parser = argparse.ArgumentParser(description="Entry processor")
    parser.add_argument(
        "--entries-dir",
        default="entries",
        help="Directory containing entry JSON files",
    )
    parser.add_argument(
        "--output",
        default="README.md",
        help="Path to the generated README file (default: README.MD)",
    )

    args = parser.parse_args()
    entries_df = pl.concat([pl.read_json(entry, schema=rna_tool_polars_schema) for entry in Path(args.entries_dir).glob("*.json")])
    entries_df = entries_df.with_columns(pl.col("date").cast(pl.Date))


    # print stats
    for col in entries_df.columns:
        dddtype = rna_tool_polars_schema[col]
        logger.info(f"Field: {col} ({dddtype})")
        if isinstance(dddtype, pl.List):
            logger.info(f"Field: {entries_df.explode(col)[col].value_counts(sort=True)}")
        else:
            logger.info(f"Field: {entries_df[col].value_counts(sort=True)}")
    #     if (col in ["name","title","description"]):
    #         entries_df = entries_df.with_columns(pl.col(col).map_elements(return_dtype=pl.String,function= lambda x: BeautifulSoup(x.strip()).getText()))
    #         if not entries_df.filter(pl.col(col).str.contains("jats")).is_empty():
    #             print("asdadsa")
    #             break
    # # entries_df = entries_df.with_columns(pl.col("date").cast(pl.String))
    # # for row in entries_df.iter_rows(named=True):
    # #     (Path("entries") / f"{row['name']}.json").write_text(
    # #         json.dumps(row, ensure_ascii=False, indent=2) + "\n",
    # #         encoding="utf-8",
    # #     )

    # Build README content
    header = readme_header()
    nav = add_nav_md(entries_df)

    # Build body with sections and topic subsections
    body_sections = []
    # Define order of sections
    type_order = [("tool", "Tools"), ("database", "Databases"), ("paper", "Papers")]
    for entry_type, display_name in type_order:
        type_entries = entries_df.filter(pl.col("type") == entry_type)
        if type_entries.height == 0:
            continue
        # Type heading with anchor
        # Insert explicit HTML anchor before the heading for reliable linking
        # Insert HTML anchor before the type heading for reliable linking
        body_sections.append(f"## {display_name} {{#{entry_type.lower()}}}")
        # (removed - merged into previous line)
        # Track seen topics to preserve order
        seen_topics = set()
        for row in type_entries.iter_rows(named=True):
            topics = row.get("topics", [])
            first_topic = topics[0].title() if topics else "Misc"
            if first_topic in seen_topics:
                continue
            seen_topics.add(first_topic)
            topic_anchor = f"{entry_type}-{first_topic}".replace(" ", "-").lower()
            # Topic subheading with anchor
            # Insert explicit HTML anchor before the subheading for reliable linking
            # Insert HTML anchor before the topic subheading for reliable linking
            body_sections.append(f"### {first_topic} {{#{topic_anchor}}}")
            # (removed - merged into previous line)
            # Add all entries that belong to this topic
            for entry in type_entries.iter_rows(named=True):
                entry_topics = entry.get("topics", [])
                entry_first = entry_topics[0].title() if entry_topics else "Misc"
                if entry_first == first_topic:
                    body_sections.append(entry_2_md(entry))
        body_sections.append("")  # blank line after each type
    body = "\n".join(body_sections)

    footer = readme_footer()
    readme_content = f"{header}\n{nav}\n{body}\n{footer}"

    # Write to the specified output file
    Path(args.output).write_text(readme_content, encoding="utf-8")


    

if __name__ == "__main__":
    main()