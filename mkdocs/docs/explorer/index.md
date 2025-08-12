# Tool Explorer

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
<option value="C++">C++</option>
<option value="Perl">Perl</option>
<option value="Python">Python</option>
</select>
</div>

<div class="filter-group">
<label for="package-filter">Package Manager:</label>
<select id="package-filter" multiple>
<option value="">All Package Managers</option>
<option value="bioconda">bioconda</option>
<option value="github">github</option>
</select>
</div>

<div class="filter-group">
<label for="platform-filter">Platform:</label>
<select id="platform-filter" multiple>
<option value="">All Platforms</option>
<option value="linux">linux</option>
<option value="macos">macos</option>
<option value="windows">windows</option>
</select>
</div>

<div class="filter-group">
<label for="topic-filter">Topic:</label>
<select id="topic-filter" multiple>
<option value="">All Topics</option>
<option value="classification">Classification</option>
<option value="cloud-computing">Cloud Computing</option>
<option value="coronavirus">Coronavirus</option>
<option value="deep-learning">Deep Learning</option>
<option value="discovery">Discovery</option>
<option value="dna-viruses">Dna Viruses</option>
<option value="genome-annotation">Genome Annotation</option>
<option value="genome-assembly">Genome Assembly</option>
<option value="high-throughput">High Throughput</option>
<option value="machine-learning">Machine Learning</option>
<option value="metagenomics">Metagenomics</option>
<option value="multi-classifier">Multi Classifier</option>
<option value="multiple-sequence-alignment">Multiple Sequence Alignment</option>
<option value="orf-prediction">Orf Prediction</option>
<option value="phylogenetics">Phylogenetics</option>
<option value="rdrp-detection">RdRp Detection</option>
<option value="rna-virus-identification">RNA Virus Identification</option>
<option value="rna-viruses">Rna Viruses</option>
<option value="specialized-assembly">Specialized Assembly</option>
<option value="taxonomy">Taxonomy</option>
<option value="viral-genomes">Viral Genomes</option>
<option value="virus-identification">Virus Identification</option>
</select>
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
<tr class="tool-row" data-language="C++" data-package-managers="bioconda" data-platforms="" data-topics="genome-assembly,coronavirus,rna-viruses,specialized-assembly">
    <td class="tool-name"><a href='https://github.com/ablab/spades' target='_blank'>coronaSPAdes</a></td>
    <td class="tool-description">Specialized assembler for coronavirus genomes and other RNA viral sequences</td>
    <td class="tool-language">C++</td>
    <td class="tool-topics"><span class='badge badge-topic'>Genome Assembly</span> <span class='badge badge-topic'>Coronavirus</span> <span class='badge badge-topic'>Rna Viruses</span> <span class='badge badge-topic'>Specialized Assembly</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-2.0</td>
    <td class="tool-version">3.15.5</td>
</tr><tr class="tool-row" data-language="Python" data-package-managers="github" data-platforms="linux,macos" data-topics="virus-identification,machine-learning,deep-learning,metagenomics">
    <td class="tool-name"><a href='https://github.com/jessieren/DeepVirFinder' target='_blank'>DeepVirFinder</a></td>
    <td class="tool-description">Deep learning method for identifying viral sequences from metagenomic data</td>
    <td class="tool-language">Python</td>
    <td class="tool-topics"><span class='badge badge-topic'>Virus Identification</span> <span class='badge badge-topic'>Machine Learning</span> <span class='badge badge-topic'>Deep Learning</span> <span class='badge badge-topic'>Metagenomics</span></td>
    <td class="tool-package">github</td>
    <td class="tool-platforms">linux, macos</td>
    <td class="tool-license">MIT</td>
    <td class="tool-version">1.0</td>
</tr><tr class="tool-row" data-language="C++" data-package-managers="bioconda" data-platforms="" data-topics="genome-assembly,rna-viruses,metagenomics,specialized-assembly">
    <td class="tool-name"><a href='https://github.com/ablab/spades' target='_blank'>metaviralSPAdes-RNA</a></td>
    <td class="tool-description">Modified metaSPAdes assembler optimized for RNA viral genome assembly from metagenomic data</td>
    <td class="tool-language">C++</td>
    <td class="tool-topics"><span class='badge badge-topic'>Genome Assembly</span> <span class='badge badge-topic'>Rna Viruses</span> <span class='badge badge-topic'>Metagenomics</span> <span class='badge badge-topic'>Specialized Assembly</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-2.0</td>
    <td class="tool-version">3.15.5</td>
</tr><tr class="tool-row" data-language="C++" data-package-managers="github" data-platforms="linux,macos,windows" data-topics="rna-virus-identification,rdrp-detection,classification,taxonomy">
    <td class="tool-name"><a href='https://github.com/rcedgar/palmscan' target='_blank'>palmID</a></td>
    <td class="tool-description">Identifies and classifies RNA virus sequences based on the conserved RdRp palm domain</td>
    <td class="tool-language">C++</td>
    <td class="tool-topics"><span class='badge badge-topic'>RNA Virus Identification</span> <span class='badge badge-topic'>RdRp Detection</span> <span class='badge badge-topic'>Classification</span> <span class='badge badge-topic'>Taxonomy</span></td>
    <td class="tool-package">github</td>
    <td class="tool-platforms">linux, macos, windows</td>
    <td class="tool-license">GPL-3.0</td>
    <td class="tool-version">1.0</td>
</tr><tr class="tool-row" data-language="Python" data-package-managers="bioconda" data-platforms="" data-topics="rna-virus-identification,rdrp-detection,metagenomics">
    <td class="tool-name"><a href='https://github.com/JustineCharon/RdRp-scan/' target='_blank'>RdRp-scan</a></td>
    <td class="tool-description">Fast profile-based detection of RNA-dependent RNA polymerase (RdRp) sequences for exploring the 'dusk matter' of the RNA virosphere</td>
    <td class="tool-language">Python</td>
    <td class="tool-topics"><span class='badge badge-topic'>RNA Virus Identification</span> <span class='badge badge-topic'>RdRp Detection</span> <span class='badge badge-topic'>Metagenomics</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">None</td>
    <td class="tool-version">None</td>
</tr><tr class="tool-row" data-language="Python" data-package-managers="bioconda" data-platforms="" data-topics="rna-virus-identification,cloud-computing,high-throughput,discovery">
    <td class="tool-name"><a href='https://github.com/ababaian/serratus' target='_blank'>Serratus</a></td>
    <td class="tool-description">Ultra-high throughput discovery of RNA viruses from public sequencing data using cloud computing</td>
    <td class="tool-language">Python</td>
    <td class="tool-topics"><span class='badge badge-topic'>RNA Virus Identification</span> <span class='badge badge-topic'>Cloud Computing</span> <span class='badge badge-topic'>High Throughput</span> <span class='badge badge-topic'>Discovery</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-3.0</td>
    <td class="tool-version">1.0</td>
</tr><tr class="tool-row" data-language="Perl" data-package-managers="bioconda" data-platforms="" data-topics="genome-annotation,orf-prediction,viral-genomes,rna-viruses">
    <td class="tool-name"><a href='https://github.com/JCVI-VIRIFX/VIGOR4' target='_blank'>VIGOR</a></td>
    <td class="tool-description">Viral genome ORF reader for annotation of viral genomes, including RNA viruses</td>
    <td class="tool-language">Perl</td>
    <td class="tool-topics"><span class='badge badge-topic'>Genome Annotation</span> <span class='badge badge-topic'>Orf Prediction</span> <span class='badge badge-topic'>Viral Genomes</span> <span class='badge badge-topic'>Rna Viruses</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-3.0</td>
    <td class="tool-version">4.1.20200702</td>
</tr><tr class="tool-row" data-language="Python" data-package-managers="bioconda" data-platforms="" data-topics="phylogenetics,multiple-sequence-alignment,viral-genomes,rna-viruses">
    <td class="tool-name"><a href='https://github.com/niemasd/ViralMSA' target='_blank'>ViralMSA</a></td>
    <td class="tool-description">Massively scalable reference-guided multiple sequence alignment of viral genomes, including RNA viruses</td>
    <td class="tool-language">Python</td>
    <td class="tool-topics"><span class='badge badge-topic'>Phylogenetics</span> <span class='badge badge-topic'>Multiple Sequence Alignment</span> <span class='badge badge-topic'>Viral Genomes</span> <span class='badge badge-topic'>Rna Viruses</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-3.0</td>
    <td class="tool-version">1.1.44</td>
</tr><tr class="tool-row" data-language="Python" data-package-managers="bioconda" data-platforms="" data-topics="virus-identification,multi-classifier,rna-viruses,dna-viruses">
    <td class="tool-name"><a href='https://github.com/jiarong/VirSorter2' target='_blank'>VirSorter2</a></td>
    <td class="tool-description">Multi-classifier approach to detect diverse DNA and RNA virus sequences</td>
    <td class="tool-language">Python</td>
    <td class="tool-topics"><span class='badge badge-topic'>Virus Identification</span> <span class='badge badge-topic'>Multi Classifier</span> <span class='badge badge-topic'>Rna Viruses</span> <span class='badge badge-topic'>Dna Viruses</span></td>
    <td class="tool-package">bioconda</td>
    <td class="tool-platforms"></td>
    <td class="tool-license">GPL-2.0</td>
    <td class="tool-version">2.2.4</td>
</tr></tbody>
</table>
</div>

<link rel="stylesheet" href="../assets/css/tool-explorer.css">
<script src="../assets/js/tool-explorer.js"></script>
