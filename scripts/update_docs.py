#!/usr/bin/env python3
"""
Update MkDocs documentation from tool entries

This script reads all JSON files from the entries/ folder and generates
the MkDocs site structure with tool explorer functionality.
"""

import polars as pl
import json
import yaml
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
ENTRIES_DIR = "entries"
MKDOCS_DIR = "mkdocs"
MKDOCS_CONFIG = f"{MKDOCS_DIR}/mkdocs.yml"
DOCS_DIR = f"{MKDOCS_DIR}/docs"
SCHEMA_FILE = "scripts/schema.json"

# Topic to category mapping with descriptions
TOPIC_CATEGORIES = {
    "rna-virus-identification": {
        "name": "RNA Virus Identification",
        "description": "Tools for detecting and identifying RNA viruses in sequencing data.",
        "icon": "🦠"
    },
    "rdrp-detection": {
        "name": "RdRp Detection", 
        "description": "Specialized tools for detecting RNA-dependent RNA polymerase sequences.",
        "icon": "🧬"
    },
    "genome-assembly": {
        "name": "Genome Assembly",
        "description": "Tools for assembling viral genomes from sequencing data.",
        "icon": "🧩"
    },
    "annotation": {
        "name": "Annotation",
        "description": "Tools for annotating viral genomes and predicting gene functions.",
        "icon": "📝"
    },
    "phylogenetics": {
        "name": "Phylogenetics",
        "description": "Tools for phylogenetic analysis and evolutionary studies of RNA viruses.",
        "icon": "🌳"
    },
    "host-prediction": {
        "name": "Host Prediction",
        "description": "Tools for predicting viral hosts and host-virus interactions.",
        "icon": "🎯"
    },
    "databases": {
        "name": "Databases",
        "description": "Databases and resources containing viral sequence data and annotations.",
        "icon": "🗄️"
    }
}

def load_entries():
    """Load all tool entries from JSON files."""
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

def extract_metadata(entries_list):
    """Extract metadata for filtering functionality."""
    if not entries_list:
        return {}
    
    metadata = {
        'languages': set(),
        'package_managers': set(),
        'platforms': set(),
        'topics': set(),
        'licenses': set(),
        'installation_methods': set()
    }
    
    for entry in entries_list:
        # Language
        if entry.get('language'):
            metadata['languages'].add(entry['language'])
        
        # Package managers (handle both old and new format)
        package_managers = entry.get('package_managers', [])
        if not package_managers and entry.get('package_manager'):
            package_managers = [entry.get('package_manager')]
        for pm in package_managers:
            metadata['package_managers'].add(pm)
        
        # Platforms
        for platform in entry.get('platforms', []):
            metadata['platforms'].add(platform)
        
        # Topics
        for topic in entry.get('topics', []):
            metadata['topics'].add(topic)
        
        # License
        if entry.get('license'):
            metadata['licenses'].add(entry['license'])
        
        # Installation methods
        for method in entry.get('installation_methods', []):
            metadata['installation_methods'].add(method)
    
    # Convert sets to sorted lists
    return {k: sorted(list(v)) for k, v in metadata.items()}







def format_tool_table_row(entry):
    """Format a single tool entry as a table row."""
    name = entry.get('name', 'Unknown')
    url = entry.get('url', '')
    description = entry.get('description', '')
    language = entry.get('language', '')
    license_info = entry.get('license', '')
    version = entry.get('version', '')
    
    # Handle both old and new package manager formats
    package_managers = entry.get('package_managers', [])
    if not package_managers and entry.get('package_manager'):
        package_managers = [entry.get('package_manager')]
    
    platforms = entry.get('platforms', [])
    topics = entry.get('topics', [])
    
    # Format name with link
    name_cell = f"<a href='{url}' target='_blank'>{name}</a>" if url else name
    
    # Format topics with badges
    topics_cell = ""
    if topics:
        topic_badges = []
        for topic in topics:
            topic_name = TOPIC_CATEGORIES.get(topic, {}).get('name', topic.replace('-', ' ').title())
            topic_badges.append(f"<span class='badge badge-topic'>{topic_name}</span>")
        topics_cell = " ".join(topic_badges)
    
    # Format package managers
    package_cell = ", ".join(package_managers) if package_managers else ""
    
    # Format platforms
    platform_cell = ", ".join(platforms) if platforms else ""
    
    # Build table row with data attributes for filtering
    row = f"""<tr class="tool-row" data-language="{language}" data-package-managers="{','.join(package_managers)}" data-platforms="{','.join(platforms)}" data-topics="{','.join(topics)}">
    <td class="tool-name">{name_cell}</td>
    <td class="tool-description">{description}</td>
    <td class="tool-language">{language}</td>
    <td class="tool-topics">{topics_cell}</td>
    <td class="tool-package">{package_cell}</td>
    <td class="tool-platforms">{platform_cell}</td>
    <td class="tool-license">{license_info}</td>
    <td class="tool-version">{version}</td>
</tr>"""
    
    return row

def format_tool_card(entry):
    """Format a single tool entry as a card (for featured tools on index page)."""
    name = entry.get('name', 'Unknown')
    url = entry.get('url', '')
    description = entry.get('description', '')
    language = entry.get('language')
    license_info = entry.get('license')
    doi = entry.get('doi')
    version = entry.get('version')
    
    # Handle both old and new package manager formats
    package_managers = entry.get('package_managers', [])
    if not package_managers and entry.get('package_manager'):
        package_managers = [entry.get('package_manager')]
    
    platforms = entry.get('platforms', [])
    installation_methods = entry.get('installation_methods', [])
    
    # Build the card
    card = f"""<div class="tool-card">
<h3>{f"<a href='{url}' target='_blank'>{name}</a>" if url else name}</h3>
<p>{description}</p>
"""
    
    # Badges
    badges = []
    if language:
        badges.append(f"<span class='badge badge-language'>{language}</span>")
    if license_info:
        badges.append(f"<span class='badge badge-license'>{license_info}</span>")
    if version:
        badges.append(f"<span class='badge badge-version'>v{version}</span>")
    for pm in package_managers:
        badges.append(f"<span class='badge badge-package'>{pm}</span>")
    if badges:
        card += "<div class='tool-badges'>" + " ".join(badges) + "</div>"
    
    # Additional info
    if platforms:
        card += f"<p><strong>Platforms:</strong> {', '.join(platforms)}</p>"
    if installation_methods:
        card += f"<p><strong>Installation:</strong> {', '.join(installation_methods)}</p>"
    if doi:
        card += f"<p><strong>DOI:</strong> <a href='https://doi.org/{doi}' target='_blank'>{doi}</a></p>"
    
    card += "</div>\n\n"
    return card

def generate_explorer_page(entries_list, metadata):
    """Generate the main tool explorer page."""
    content = f"""# Tool Explorer

Explore RNA virus tools by category, programming language, package manager, and more.

<div class="explorer-controls">
<div class="search-box">
<input type="text" id="tool-search" placeholder="Search tools..." />
</div>

<div class="filters-row">
<div class="filter-group">
<label for="language-filter">Language:</label>
<select id="language-filter" multiple>
<option value="">All Languages</option>
"""
    
    for lang in metadata['languages']:
        content += f'<option value="{lang}">{lang}</option>\n'
    
    content += """</select>
</div>

<div class="filter-group">
<label for="package-filter">Package Manager:</label>
<select id="package-filter" multiple>
<option value="">All Package Managers</option>
"""
    
    for pm in metadata['package_managers']:
        content += f'<option value="{pm}">{pm}</option>\n'
    
    content += """</select>
</div>

<div class="filter-group">
<label for="platform-filter">Platform:</label>
<select id="platform-filter" multiple>
<option value="">All Platforms</option>
"""
    
    for platform in metadata['platforms']:
        content += f'<option value="{platform}">{platform}</option>\n'
    
    content += """</select>
</div>

<div class="filter-group">
<label for="topic-filter">Topic:</label>
<select id="topic-filter" multiple>
<option value="">All Topics</option>
"""
    
    for topic in metadata['topics']:
        topic_name = TOPIC_CATEGORIES.get(topic, {}).get('name', topic.replace('-', ' ').title())
        content += f'<option value="{topic}">{topic_name}</option>\n'
    
    content += """</select>
</div>

<div class="filter-group">
<button id="clear-filters">Clear All Filters</button>
</div>
</div>
</div>

<div id="tool-count">Showing all tools</div>

<div class="table-container">
<table id="tools-table" class="tools-table">
<thead>
    <tr>
        <th class="sortable" data-column="name">Tool Name</th>
        <th class="sortable" data-column="description">Description</th>
        <th class="sortable" data-column="language">Language</th>
        <th class="sortable" data-column="topics">Topics</th>
        <th class="sortable" data-column="package">Package Manager</th>
        <th class="sortable" data-column="platforms">Platforms</th>
        <th class="sortable" data-column="license">License</th>
        <th class="sortable" data-column="version">Version</th>
    </tr>
</thead>
<tbody id="tools-container">
"""
    
    # Add all tools
    for entry in sorted(entries_list, key=lambda x: x.get('name', '').lower()):
        content += format_tool_table_row(entry)
    
    content += """</tbody>
</table>
</div>

<link rel="stylesheet" href="../assets/css/tool-explorer.css">
<script src="../assets/js/tool-explorer.js"></script>
"""
    
    return content



def generate_index_page(entries_list, categories):
    """Generate the main index page."""
    total_tools = len(entries_list)
    total_categories = len([cat for cat in categories if cat in TOPIC_CATEGORIES])
    
    content = f"""# Awesome RNA Virus Tools

Welcome to the comprehensive collection of tools, databases, and resources for RNA virus research.

## 📊 Overview

- **{total_tools}** curated tools and resources
- **{total_categories}** specialized categories
- **Community-driven** curation and maintenance

## 🚀 Quick Start

<div class="quick-start-grid">
<div class="quick-start-card">
<h3>🔍 Explore Tools</h3>
<p>Browse our interactive tool explorer with advanced filtering capabilities.</p>
<a href="explorer/" class="btn btn-primary">Explore Tools</a>
</div>

<div class="quick-start-card">
<h3>📚 Browse by Category</h3>
<p>Find tools organized by research area and functionality.</p>
<a href="#categories" class="btn btn-secondary">View Categories</a>
</div>

<div class="quick-start-card">
<h3>🤝 Contribute</h3>
<p>Help us grow the collection by adding new tools and resources.</p>
<a href="../contributing/guidelines/" class="btn btn-tertiary">Contribute</a>
</div>
</div>

## 📂 Categories {{#categories}}

<div class="categories-grid">
"""
    
    for topic, category_info in TOPIC_CATEGORIES.items():
        if topic not in categories:
            continue
        
        name = category_info['name']
        description = category_info['description']
        icon = category_info.get('icon', '🔬')
        tool_count = len(categories[topic])
        
        content += f"""
<div class="category-card">
<h3>{icon} <a href="tools/{topic}/">{name}</a></h3>
<p>{description}</p>
<div class="tool-count">{tool_count} tools</div>
</div>
"""
    
    content += """</div>

## 🌟 Featured Tools

Here are some highlighted tools from our collection:

"""
    
    # Add a few featured tools (most recent or popular)
    featured_tools = sorted(entries_list, key=lambda x: x.get('date', ''), reverse=True)[:3]
    
    for tool in featured_tools:
        content += format_tool_card(tool)
    
    content += """
## 📈 Statistics

<div class="stats-grid">
<div class="stat-card">
<h4>Programming Languages</h4>
<div class="stat-value">{}</div>
</div>

<div class="stat-card">
<h4>Package Managers</h4>
<div class="stat-value">{}</div>
</div>

<div class="stat-card">
<h4>Platforms Supported</h4>
<div class="stat-value">{}</div>
</div>
</div>

---

*Last updated: {}*
""".format(
        len(set(entry.get('language') for entry in entries_list if entry.get('language'))),
        len(set(pm for entry in entries_list for pm in (entry.get('package_managers', []) or [entry.get('package_manager')] if entry.get('package_manager') else []))),
        len(set(platform for entry in entries_list for platform in entry.get('platforms', []))),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    )
    
    return content

def generate_tools_data_json(entries_list):
    """Generate JSON data file for JavaScript filtering."""
    # Clean up data for JSON export
    tools_data = []
    for entry in entries_list:
        # Handle package managers (both old and new format)
        package_managers = entry.get('package_managers', [])
        if not package_managers and entry.get('package_manager'):
            package_managers = [entry.get('package_manager')]
        
        tool_data = {
            'name': entry.get('name', ''),
            'url': entry.get('url', ''),
            'description': entry.get('description', ''),
            'language': entry.get('language', ''),
            'license': entry.get('license', ''),
            'version': entry.get('version', ''),
            'doi': entry.get('doi', ''),
            'topics': entry.get('topics', []),
            'package_managers': package_managers,
            'platforms': entry.get('platforms', []),
            'installation_methods': entry.get('installation_methods', []),
            'date': entry.get('date', '')
        }
        tools_data.append(tool_data)
    
    return tools_data

def generate_tool_explorer_js(metadata):
    """Generate the tool explorer JavaScript file with updated topic categories."""
    # Convert TOPIC_CATEGORIES to JavaScript object
    topic_categories_js = "{"
    for topic, info in TOPIC_CATEGORIES.items():
        topic_categories_js += f'\n        "{topic}": "{info["name"]}",'
    topic_categories_js = topic_categories_js.rstrip(',') + "\n    }"
    
    js_content = f"""/**
 * Tool Explorer JavaScript
 * Interactive filtering and search functionality for RNA virus tools
 */

class ToolExplorer {{
    constructor() {{
        this.tools = [];
        this.filteredTools = [];
        this.filters = {{
            search: '',
            language: [],
            packageManager: [],
            platform: [],
            topic: []
        }};
        
        this.topicCategories = {topic_categories_js};
        
        this.init();
    }}
    
    async init() {{
        try {{
            // Load tools data
            const response = await fetch('../assets/js/tools-data.json');
            this.tools = await response.json();
            this.filteredTools = [...this.tools];
            
            this.setupEventListeners();
            this.updateDisplay();
        }} catch (error) {{
            console.error('Failed to load tools data:', error);
        }}
    }}
    
    setupEventListeners() {{
        // Search input
        const searchInput = document.getElementById('tool-search');
        if (searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                this.filters.search = e.target.value.toLowerCase();
                this.applyFilters();
            }});
        }}
        
        // Filter selects
        const languageFilter = document.getElementById('language-filter');
        if (languageFilter) {{
            languageFilter.addEventListener('change', () => {{
                this.filters.language = Array.from(languageFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            }});
        }}
        
        const packageFilter = document.getElementById('package-filter');
        if (packageFilter) {{
            packageFilter.addEventListener('change', () => {{
                this.filters.packageManager = Array.from(packageFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            }});
        }}
        
        const platformFilter = document.getElementById('platform-filter');
        if (platformFilter) {{
            platformFilter.addEventListener('change', () => {{
                this.filters.platform = Array.from(platformFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            }});
        }}
        
        const topicFilter = document.getElementById('topic-filter');
        if (topicFilter) {{
            topicFilter.addEventListener('change', () => {{
                this.filters.topic = Array.from(topicFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            }});
        }}
        
        // Clear filters button
        const clearButton = document.getElementById('clear-filters');
        if (clearButton) {{
            clearButton.addEventListener('click', () => {{
                this.clearAllFilters();
            }});
        }}
    }}
    
    applyFilters() {{
        this.filteredTools = this.tools.filter(tool => {{
            // Search filter
            if (this.filters.search) {{
                const searchTerm = this.filters.search;
                const searchableText = [
                    tool.name,
                    tool.description,
                    ...(tool.topics || [])
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchTerm)) {{
                    return false;
                }}
            }}
            
            // Language filter
            if (this.filters.language.length > 0) {{
                if (!tool.language || !this.filters.language.includes(tool.language)) {{
                    return false;
                }}
            }}
            
            // Package manager filter
            if (this.filters.packageManager.length > 0) {{
                const toolPackageManagers = tool.package_managers || [];
                if (!this.filters.packageManager.some(pm => toolPackageManagers.includes(pm))) {{
                    return false;
                }}
            }}
            
            // Platform filter
            if (this.filters.platform.length > 0) {{
                const toolPlatforms = tool.platforms || [];
                if (!this.filters.platform.some(platform => toolPlatforms.includes(platform))) {{
                    return false;
                }}
            }}
            
            // Topic filter
            if (this.filters.topic.length > 0) {{
                const toolTopics = tool.topics || [];
                if (!this.filters.topic.some(topic => toolTopics.includes(topic))) {{
                    return false;
                }}
            }}
            
            return true;
        }});
        
        this.updateDisplay();
    }}
    
    updateDisplay() {{
        this.updateToolCount();
        this.renderTools();
    }}
    
    updateToolCount() {{
        const countElement = document.getElementById('tool-count');
        if (countElement) {{
            const total = this.tools.length;
            const filtered = this.filteredTools.length;
            
            if (filtered === total) {{
                countElement.textContent = `Showing all ${{total}} tools`;
            }} else {{
                countElement.textContent = `Showing ${{filtered}} of ${{total}} tools`;
            }}
        }}
    }}
    
    renderTools() {{
        const container = document.getElementById('tools-container');
        if (!container) return;
        
        if (this.filteredTools.length === 0) {{
            container.innerHTML = `
                <tr class="no-results">
                    <td colspan="8" style="text-align: center; padding: 2rem;">
                        <h3>No tools found</h3>
                        <p>Try adjusting your filters or search terms.</p>
                    </td>
                </tr>
            `;
            return;
        }}
        
        // Sort tools alphabetically
        const sortedTools = [...this.filteredTools].sort((a, b) => 
            (a.name || '').localeCompare(b.name || '')
        );
        
        container.innerHTML = sortedTools.map(tool => this.renderToolRow(tool)).join('');
    }}
    
    renderToolRow(tool) {{
        const name = tool.name || 'Unknown';
        const url = tool.url || '';
        const description = tool.description || '';
        const language = tool.language || '';
        const license = tool.license || '';
        const version = tool.version || '';
        const packageManagers = tool.package_managers || [];
        const platforms = tool.platforms || [];
        const topics = tool.topics || [];
        
        // Format name with link
        const nameCell = url ? `<a href="${{url}}" target="_blank">${{name}}</a>` : name;
        
        // Format topics with badges
        const topicsCell = topics.map(topic => {{
            const topicName = this.topicCategories[topic] || topic.replace('-', ' ').replace(/\\b\\w/g, l => l.toUpperCase());
            return `<span class="badge badge-topic">${{topicName}}</span>`;
        }}).join(' ');
        
        // Format package managers and platforms
        const packageCell = packageManagers.join(', ');
        const platformCell = platforms.join(', ');
        
        return `
            <tr class="tool-row" 
                data-language="${{language}}" 
                data-package-managers="${{packageManagers.join(',')}}" 
                data-platforms="${{platforms.join(',')}}" 
                data-topics="${{topics.join(',')}}">
                <td class="tool-name">${{nameCell}}</td>
                <td class="tool-description">${{description}}</td>
                <td class="tool-language">${{language}}</td>
                <td class="tool-topics">${{topicsCell}}</td>
                <td class="tool-package">${{packageCell}}</td>
                <td class="tool-platforms">${{platformCell}}</td>
                <td class="tool-license">${{license}}</td>
                <td class="tool-version">${{version}}</td>
            </tr>
        `;
    }}
    
    clearAllFilters() {{
        // Reset all filters
        this.filters = {{
            search: '',
            language: [],
            packageManager: [],
            platform: [],
            topic: []
        }};
        
        // Reset form elements
        const searchInput = document.getElementById('tool-search');
        if (searchInput) searchInput.value = '';
        
        const selects = [
            'language-filter',
            'package-filter', 
            'platform-filter',
            'topic-filter'
        ];
        
        selects.forEach(selectId => {{
            const select = document.getElementById(selectId);
            if (select) {{
                Array.from(select.options).forEach(option => {{
                    option.selected = false;
                }});
            }}
        }});
        
        // Reapply filters (which will show all tools)
        this.applyFilters();
    }}
}}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {{
    new ToolExplorer();
}});

// Re‑initialize on MkDocs Material SPA navigation
document.addEventListener('mkdocs:page:changed', () => {{
    // Only initialize if the explorer container exists on the new page
    if (document.getElementById('tools-container')) {{
        new ToolExplorer();
    }}
}});
"""
    
    # Write the JavaScript file
    with open(f"{DOCS_DIR}/assets/js/tool-explorer.js", 'w') as f:
        f.write(js_content)

def update_mkdocs_config(categories):
    """Update the mkdocs.yml configuration file."""
    config_path = Path(MKDOCS_CONFIG)
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"MkDocs config file not found: {config_path}")
        return
    
    # Update navigation structure
    nav = [
        {'Home': 'index.md'},
        {'Explorer': 'explorer/index.md'},
        {'About': 'about/index.md'},
        {'Contributing': 'contributing/guidelines.md'}
    ]
    
    config['nav'] = nav
    
    # Write updated config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    logger.info(f"Updated MkDocs configuration: {config_path}")

def create_directory_structure():
    """Create necessary directory structure."""
    dirs_to_create = [
        f"{DOCS_DIR}/explorer",
        f"{DOCS_DIR}/assets/js",
        f"{DOCS_DIR}/assets/css"
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {dir_path}")
    
    # Clean up old topic pages
    tools_dir = Path(f"{DOCS_DIR}/tools")
    if tools_dir.exists():
        import shutil
        shutil.rmtree(tools_dir)
        logger.info("Removed old topic pages directory")

def main():
    """Main entry point."""
    logger.info("Starting MkDocs documentation generation")
    
    # Create directory structure
    create_directory_structure()
    
    # Load entries
    entries_list = load_entries()
    if not entries_list:
        logger.error("No entries found, exiting")
        return
    
    # Categorize entries and extract metadata
    categories = categorize_entries(entries_list)
    metadata = extract_metadata(entries_list)
    
    # Generate main index page
    index_content = generate_index_page(entries_list, categories)
    with open(f"{DOCS_DIR}/index.md", 'w') as f:
        f.write(index_content)
    logger.info("Generated index page")
    
    # Generate explorer page
    explorer_content = generate_explorer_page(entries_list, metadata)
    with open(f"{DOCS_DIR}/explorer/index.md", 'w') as f:
        f.write(explorer_content)
    logger.info("Generated explorer page")
    
    # Generate tools data JSON for JavaScript
    tools_data = generate_tools_data_json(entries_list)
    with open(f"{DOCS_DIR}/assets/js/tools-data.json", 'w') as f:
        json.dump(tools_data, f, indent=2)
    logger.info("Generated tools data JSON")
    
    # Generate updated JavaScript with topic categories
    generate_tool_explorer_js(metadata)
    logger.info("Generated tool explorer JavaScript")
    
    # Update MkDocs configuration
    update_mkdocs_config(categories)
    
    logger.info("MkDocs documentation generation completed")

if __name__ == "__main__":
    main()