/**
 * Tool Explorer JavaScript
 * Interactive filtering and search functionality for RNA virus tools
 */

class ToolExplorer {
    constructor() {
        this.tools = [];
        this.filteredTools = [];
        this.filters = {
            search: '',
            language: [],
            packageManager: [],
            platform: [],
            topic: []
        };
        
        this.topicCategories = {
        "rna-virus-identification": "RNA Virus Identification",
        "rdrp-detection": "RdRp Detection",
        "genome-assembly": "Genome Assembly",
        "annotation": "Annotation",
        "phylogenetics": "Phylogenetics",
        "host-prediction": "Host Prediction",
        "databases": "Databases"
    };
        
        this.init();
    }
    
    async init() {
        try {
            // Load tools data
            const response = await fetch('../assets/js/tools-data.json');
            this.tools = await response.json();
            this.filteredTools = [...this.tools];
            
            this.setupEventListeners();
            this.updateDisplay();
        } catch (error) {
            console.error('Failed to load tools data:', error);
        }
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('tool-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filters.search = e.target.value.toLowerCase();
                this.applyFilters();
            });
        }
        
        // Filter selects
        const languageFilter = document.getElementById('language-filter');
        if (languageFilter) {
            languageFilter.addEventListener('change', () => {
                this.filters.language = Array.from(languageFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            });
        }
        
        const packageFilter = document.getElementById('package-filter');
        if (packageFilter) {
            packageFilter.addEventListener('change', () => {
                this.filters.packageManager = Array.from(packageFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            });
        }
        
        const platformFilter = document.getElementById('platform-filter');
        if (platformFilter) {
            platformFilter.addEventListener('change', () => {
                this.filters.platform = Array.from(platformFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            });
        }
        
        const topicFilter = document.getElementById('topic-filter');
        if (topicFilter) {
            topicFilter.addEventListener('change', () => {
                this.filters.topic = Array.from(topicFilter.selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                this.applyFilters();
            });
        }
        
        // Clear filters button
        const clearButton = document.getElementById('clear-filters');
        if (clearButton) {
            clearButton.addEventListener('click', () => {
                this.clearAllFilters();
            });
        }
    }
    
    applyFilters() {
        this.filteredTools = this.tools.filter(tool => {
            // Search filter
            if (this.filters.search) {
                const searchTerm = this.filters.search;
                const searchableText = [
                    tool.name,
                    tool.description,
                    ...(tool.topics || [])
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchTerm)) {
                    return false;
                }
            }
            
            // Language filter
            if (this.filters.language.length > 0) {
                if (!tool.language || !this.filters.language.includes(tool.language)) {
                    return false;
                }
            }
            
            // Package manager filter
            if (this.filters.packageManager.length > 0) {
                const toolPackageManagers = tool.package_managers || [];
                if (!this.filters.packageManager.some(pm => toolPackageManagers.includes(pm))) {
                    return false;
                }
            }
            
            // Platform filter
            if (this.filters.platform.length > 0) {
                const toolPlatforms = tool.platforms || [];
                if (!this.filters.platform.some(platform => toolPlatforms.includes(platform))) {
                    return false;
                }
            }
            
            // Topic filter
            if (this.filters.topic.length > 0) {
                const toolTopics = tool.topics || [];
                if (!this.filters.topic.some(topic => toolTopics.includes(topic))) {
                    return false;
                }
            }
            
            return true;
        });
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        this.updateToolCount();
        this.renderTools();
    }
    
    updateToolCount() {
        const countElement = document.getElementById('tool-count');
        if (countElement) {
            const total = this.tools.length;
            const filtered = this.filteredTools.length;
            
            if (filtered === total) {
                countElement.textContent = `Showing all ${total} tools`;
            } else {
                countElement.textContent = `Showing ${filtered} of ${total} tools`;
            }
        }
    }
    
    renderTools() {
        const container = document.getElementById('tools-container');
        if (!container) return;
        
        if (this.filteredTools.length === 0) {
            container.innerHTML = `
                <tr class="no-results">
                    <td colspan="8" style="text-align: center; padding: 2rem;">
                        <h3>No tools found</h3>
                        <p>Try adjusting your filters or search terms.</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        // Sort tools alphabetically
        const sortedTools = [...this.filteredTools].sort((a, b) => 
            (a.name || '').localeCompare(b.name || '')
        );
        
        container.innerHTML = sortedTools.map(tool => this.renderToolRow(tool)).join('');
    }
    
    renderToolRow(tool) {
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
        const nameCell = url ? `<a href="${url}" target="_blank">${name}</a>` : name;
        
        // Format topics with badges
        const topicsCell = topics.map(topic => {
            const topicName = this.topicCategories[topic] || topic.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
            return `<span class="badge badge-topic">${topicName}</span>`;
        }).join(' ');
        
        // Format package managers and platforms
        const packageCell = packageManagers.join(', ');
        const platformCell = platforms.join(', ');
        
        return `
            <tr class="tool-row" 
                data-language="${language}" 
                data-package-managers="${packageManagers.join(',')}" 
                data-platforms="${platforms.join(',')}" 
                data-topics="${topics.join(',')}">
                <td class="tool-name">${nameCell}</td>
                <td class="tool-description">${description}</td>
                <td class="tool-language">${language}</td>
                <td class="tool-topics">${topicsCell}</td>
                <td class="tool-package">${packageCell}</td>
                <td class="tool-platforms">${platformCell}</td>
                <td class="tool-license">${license}</td>
                <td class="tool-version">${version}</td>
            </tr>
        `;
    }
    
    clearAllFilters() {
        // Reset all filters
        this.filters = {
            search: '',
            language: [],
            packageManager: [],
            platform: [],
            topic: []
        };
        
        // Reset form elements
        const searchInput = document.getElementById('tool-search');
        if (searchInput) searchInput.value = '';
        
        const selects = [
            'language-filter',
            'package-filter', 
            'platform-filter',
            'topic-filter'
        ];
        
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                Array.from(select.options).forEach(option => {
                    option.selected = false;
                });
            }
        });
        
        // Reapply filters (which will show all tools)
        this.applyFilters();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ToolExplorer();
});

// Re‑initialize on MkDocs Material SPA navigation
document.addEventListener('mkdocs:page:changed', () => {
    // Only initialize if the explorer container exists on the new page
    if (document.getElementById('tools-container')) {
        new ToolExplorer();
    }
});
