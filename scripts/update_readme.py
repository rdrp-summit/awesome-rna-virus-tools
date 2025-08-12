#!/usr/bin/env python3
"""
Update the main README.md file from tool entries

This script reads all JSON files from the entries/ folder using polars
and generates the main README.md file with categorized tool listings.
"""

import polars as pl
import json
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
ENTRIES_DIR = "entries"
README_FILE = "README.md"
SCHEMA_FILE = "scripts/schema.json"

# Topic to category mapping - these are boilerplates (with description)
TOPIC_CATEGORIES = {
    "rna-virus-identification": {
        "name": "RNA Virus Identification",
        "description": "Tools for detecting and identifying RNA viruses in sequencing data."
    },
    "rdrp-detection": {
        "name": "RdRp Detection", 
        "description": "Specialized tools for detecting RNA-dependent RNA polymerase sequences."
    },
    "genome-assembly": {
        "name": "Genome Assembly",
        "description": "Tools for assembling viral genomes from sequencing data."
    },
    "annotation": {
        "name": "Annotation",
        "description": "Tools for annotating viral genomes and predicting gene functions."
    },
    "phylogenetics": {
        "name": "Phylogenetics",
        "description": "Tools for phylogenetic analysis and evolutionary studies of RNA viruses."
    },
    "host-prediction": {
        "name": "Host Prediction",
        "description": "Tools for predicting viral hosts and host-virus interactions."
    },
    "databases": {
        "name": "Databases",
        "description": "Databases and resources containing viral sequence data and annotations."
    }
}

def load_entries():
    """Load all tool entries from JSON files. Failing entries are assumed to be broken."""
    entries_path = Path(ENTRIES_DIR)
    
    all_entries = []
    
    for json_file in entries_path.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                entry_data = json.load(f)
            
            # Add filename for reference
            entry_data["_filename"] = json_file.stem
            all_entries.append(entry_data)
            logger.debug(f"Loaded entry from: {json_file}")
        except Exception as e:
            logger.error(f"Failed to load {json_file}: {e}")
    
    if not all_entries:
        logger.warning("No entries loaded")
        return []
    
    logger.info(f"Loaded {len(all_entries)} tool entries")
    return all_entries

def categorize_entries(entries_list):
    """Categorize entries by their topics."""
    if not entries_list:
        return {}
    
    categories = defaultdict(list)
    
    for entry in entries_list:
        topics = entry.get('topics', [])
        if not topics:
            logger.warning(f"Entry {entry.get('name')} has no topics")
            continue
            
        # Add to each topic category
        for topic in topics:
            categories[topic].append(entry)
    
    return categories

def format_tool_entry(entry):
    """Format a single tool entry for markdown."""
    name = entry.get('name', 'Unknown')
    url = entry.get('url', '')
    description = entry.get('description', '')
    language = entry.get('language')
    license_info = entry.get('license')
    doi = entry.get('doi')
    
    # Handle both old 'package_manager' and new 'package_managers' fields
    package_managers = entry.get('package_managers', [])
    if not package_managers and entry.get('package_manager'):
        package_managers = [entry.get('package_manager')]
    
    platforms = entry.get('platforms', [])
    installation_methods = entry.get('installation_methods', [])
    
    # Build the entry line
    if url:
        entry_line = f"- **[{name}]({url})**"
    else:
        entry_line = f"- **{name}**"
    
    if description:
        entry_line += f" - {description}"
    
    # Add metadata
    metadata = []
    if language:
        metadata.append(f"Language: {language}")
    if license_info:
        metadata.append(f"License: {license_info}")
    if package_managers:
        pkg_str = ", ".join(package_managers)
        metadata.append(f"Install: {pkg_str}")
    if platforms:
        platform_str = ", ".join(platforms)
        metadata.append(f"Platforms: {platform_str}")
    if installation_methods:
        install_str = ", ".join(installation_methods)
        metadata.append(f"Methods: {install_str}")
    if doi:
        metadata.append(f"DOI: [{doi}](https://doi.org/{doi})")
    
    if metadata:
        entry_line += f" ({', '.join(metadata)})"
    
    return entry_line

def generate_readme_header():
    """Generate the header section of the README."""
    return """# Awesome RNA Virus Tools

![RdRp Summit Logo](assets/awesome-rna-virus-tools-hex.png)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Website](https://img.shields.io/website?url=https%3A//rdrp-summit.github.io/awesome-rna-virus-tools/)](https://rdrp-summit.github.io/awesome-rna-virus-tools/)
[![GitHub](https://img.shields.io/github/license/rdrp-summit/awesome-rna-virus-tools)](LICENSE)

A curated list of software, tools, databases and resources for RNA virus analysis, prediction, annotation, phylogenetics, and related research. This project builds upon the excellent [awesome-virome](https://github.com/shandley/awesome-virome) list.

🌐 **[Visit the interactive website](https://rdrp-summit.github.io/awesome-rna-virus-tools/)** to explore tools by categories, programming languages, and installation methods.

## Quick Navigation

"""

def generate_readme_footer():
    """Generate the footer section of the README."""
    return """\n
## Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for details on how to add new tools or improve existing entries.

### How to Add a Tool

1. Create a new JSON file in the `entries/` directory
2. Follow the schema defined in `scripts/schema.json`
3. Run `python scripts/update_readme.py` to update this README
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [awesome-virome](https://github.com/shandley/awesome-virome) project
- Built with ❤️ by the RNA virus research community

---

*Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """*
"""

def generate_readme(categories):
    """Generate the main README.md file."""
    readme_content = generate_readme_header()
    
    # Generate table of contents
    for topic, category_info in TOPIC_CATEGORIES.items():
        if topic in categories:
            name = category_info['name']
            anchor = name.lower().replace(' ', '-').replace('/', '-').replace('&', 'and')
            readme_content += f"- [{name}](#{anchor})\n"
    
    readme_content += "- [Contributing](#contributing)\n\n"
    
    # Generate sections
    for topic, category_info in TOPIC_CATEGORIES.items():
        if topic not in categories:
            continue
            
        name = category_info['name']
        description = category_info['description']
        tools = categories[topic]
        
        readme_content += f"## {name}\n\n{description}\n\n"
        
        # Sort tools alphabetically
        tools.sort(key=lambda x: x.get('name', '').lower())
        
        for tool in tools:
            readme_content += format_tool_entry(tool) + "\n"
        
        readme_content += "\n"
    
    # Add footer
    readme_content += generate_readme_footer()
    
    # Write README
    with open(README_FILE, 'w') as f:
        f.write(readme_content)
    
    logger.info(f"Generated {README_FILE}")

def main():
    """Main entry point."""
    logger.info("Starting README generation")
    
    # Load entries
    entries_list = load_entries()
    if not entries_list:
        logger.error("No entries found, exiting")
        return
    
    # Categorize entries
    categories = categorize_entries(entries_list)
    
    # Generate README
    generate_readme(categories)
    
    logger.info("README generation completed")

if __name__ == "__main__":
    main()