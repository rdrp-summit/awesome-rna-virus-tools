# Candidate review: 2026-08-31

This is a research ledger, not catalog data. It records the evidence used to
review candidates and whether they were promoted to `entries/`. Every candidate
below was checked against the current entry names, URLs, and DOIs; no duplicates
were found before promotion.

Status meanings:

- `added`: primary sources verify the resource and it has been promoted to the
  catalog.
- `candidate`: primary sources verify a reusable resource that is ready for a
  catalog-scope decision.
- `hold`: the resource is relevant, but access, licensing, maintenance, or
  provenance should be resolved before promotion.
- `reject`: investigated and currently unsuitable for the catalog.

## Added

### RdRpCATCH

- **Kind:** tool and database bundle
- **Purpose:** Searches nucleotide or protein FASTA input for divergent RNA
  virus RdRPs using a unified collection of profile HMM databases, then adds
  MMseqs2-based Riboviria taxonomy.
- **Source:** https://github.com/dimitris-karapliafis/RdRpCATCH
- **Web interface:** https://rdrpcatch.bioinformatics.nl
- **Publication:** https://doi.org/10.1093/nargab/lqag076
- **Version evidence:** GitHub v1.0.2, released 2026-06-09; PyPI latest is
  1.0.1.post1, uploaded 2026-02-13.
- **License / language:** MIT; Python; requires Python 3.12 or newer.
- **Installation:** Bioconda or PyPI; databases are downloaded from Zenodo by
  the CLI. Supports custom pressed pHMM databases.
- **Confidence:** high
- **Review note:** Added to `entries/rdrpcatch.json`. The repository, package metadata,
  database manager, web server, releases, and RNA-virus-specific purpose are
  independently verifiable.

### VITAP

- **Kind:** tool
- **Purpose:** Classifies DNA and RNA viral fragments, including fragments as
  short as 1 kb, using alignment, a graph algorithm, and confidence scores.
- **Source:** https://github.com/DrKaiyangZheng/VITAP
- **Publication:** https://doi.org/10.1038/s41467-025-57500-7
- **Software archive:** https://doi.org/10.5281/zenodo.14873987
- **Version evidence:** v1.12, released and archived 2026-04-16.
- **License / language:** GPL-3.0-only; Python.
- **Installation:** Bioconda/Conda environment or source clone; runs on Linux
  and macOS. Current releases build their reference data from ICTV and UniRef90.
- **Confidence:** high
- **Review note:** Added to `entries/vitap.json` as a general viral taxonomy
  tool with explicit RNA virus support, rather than as RNA-virus-only software.

### SegFinder

- **Kind:** tool/workflow
- **Purpose:** Finds complete segmented RNA virus genomes across multiple
  metatranscriptomic libraries using segment co-occurrence and correlated
  abundance, including segments without recognizable sequence homology.
- **Source:** https://github.com/Kongloner/SegFinder
- **Publication:** https://doi.org/10.1093/bib/bbaf358
- **Software archive:** https://figshare.com/articles/software/_b_SegFinder_software_code_b_/26770885
- **Publication date:** 2025-07-24 online; journal issue July 2025.
- **Version evidence:** No tagged GitHub release. The paper and Figshare archive
  are the stable provenance points.
- **License / language:** MIT; primarily Python, with Shell, R, and Perl.
- **Installation:** Conda environment or Singularity image. The workflow also
  requires large local NR/NT and taxonomy databases.
- **Confidence:** high
- **Review note:** Added to `entries/segfinder.json`. The published benchmark
  reports about 231 GB peak memory, so this remains a resource-intensive tool.

### HI-FEVER

- **Kind:** Nextflow workflow
- **Purpose:** Discovers and annotates endogenous viral elements in eukaryotic
  host genomes from viral protein queries; this includes non-retroviral RNA
  virus-derived elements but is not restricted to RNA viruses.
- **Source:** https://github.com/PaleovirologyLab/hi-fever
- **Publication:** https://doi.org/10.1093/bioinformatics/btaf610
- **Version evidence:** v0.2, released 2025-02-05; paper published online
  2025-11-08.
- **License / language:** MIT; Nextflow DSL2 with Python helpers.
- **Installation:** Conda or Pixi; Nextflow profiles support Conda and
  Apptainer. Linux is the primary platform, with macOS and WSL documented.
- **Confidence:** high
- **Review note:** Added to `entries/hi-fever.json`. Its explicit support for
  non-retroviral RNA virus-derived EVEs establishes catalog relevance.

### detectEVE

- **Kind:** Snakemake workflow
- **Purpose:** Detects non-retroviral endogenous viral elements from RNA and DNA
  viruses in genomic assemblies using similarity searches and confidence scores.
- **Source:** https://github.com/thackl/detectEVE
- **Publication:** https://doi.org/10.1111/1755-0998.14083
- **Version evidence:** v1.4.1, released 2025-02-06.
- **License / language:** MIT; Python with R, Perl, and Shell components.
- **Installation:** Conda or Mamba; input may be local FASTA or NCBI WGS
  accessions.
- **Confidence:** high
- **Review note:** Added to `entries/detecteve.json`.

### detectADAM

- **Kind:** Snakemake workflow
- **Purpose:** Mines public sequencing datasets for viral sequences by
  downloading reads, optionally masking host and EVE sequences, assembling
  unmapped reads, and searching translated contigs with DIAMOND.
- **Source:** https://github.com/LequimeLab/detectADAM
- **Version evidence:** No tagged release; repository documentation identifies
  it as a 2025 master's project.
- **License / language:** MIT; Python/Snakemake.
- **Installation:** Conda or Mamba; accepts SRA accessions or pre-downloaded
  FASTQ files.
- **Confidence:** medium-high; no peer-reviewed software paper or tagged release.
- **Review note:** Added to `entries/detectadam.json` with DOI and version left
  null rather than inferred.

### MetaVR

- **Kind:** database and web/API resource
- **Resource:** https://meta-virome.org/
- **Publication:** https://doi.org/10.1093/nar/gkaf1283
- **Evidence:** The portal identifies itself as the successor to IMG/VR 4.0 and
  exposes 24,435,662 UViGs, bulk IMGVR5 downloads, and a documented REST API.
  Its OpenAPI `GenomeType` enum explicitly includes `dsRNA`, `ssRNA`,
  `ssRNA-RT`, `ssRNA(-)`, `ssRNA(+)`, and `ssRNA(+/-)` filters, while the paper
  documents assignment to Baltimore classes.
- **Confidence:** high
- **Review note:** Added to `entries/metavr.json`. The earlier rejection was
  reversed after checking the API schema rather than only the landing page.

### VOGDB

- **Kind:** database and downloadable reference collection
- **Purpose:** Organizes RefSeq viral proteins into sequence-, profile-, and
  structure-based orthologous groups for annotation, remote homology search,
  and phylogenetic inference.
- **Resource:** https://vogdb.org/
- **Publication:** https://doi.org/10.3390/v16081191
- **RNA relevance:** Includes eukaryotic RNA viruses and RNA phages and
  explicitly handles viral polyproteins, but is not RNA-virus-specific.
- **Version evidence:** Release 236, dated 2026-07-15, follows RefSeq release
  236. VOGDB documents an approximately bimonthly update schedule.
- **License / access:** CC BY 4.0. Versioned FASTA, TSV, HMMER3, alignment,
  structure, annotation, taxonomy, host, checksum, and release JSON files are
  available for download.
- **Confidence:** very high
- **Review note:** Added to `entries/vogdb.json`, using the release date as
  `date` and adding `data_updated` for the bimonthly refresh cadence.

### Viro3D

- **Kind:** database, web portal, REST API, and downloadable datasets
- **Purpose:** Provides predicted protein structures, clusters, annotations,
  and similarity networks for human and animal viruses.
- **Resource:** https://viro3d.cvr.gla.ac.uk/
- **API:** https://viro3d.cvr.gla.ac.uk/docs
- **Publication:** https://doi.org/10.1038/s44320-025-00147-9
- **RNA relevance:** Broad-virus rather than RNA-only, with explicit Riboviria,
  RdRp, reverse-transcriptase, and viral fusion-protein coverage.
- **Version evidence:** Data released 2025-07-03; paper published online
  2025-09-16. The publication reports 85,162 proteins from 4,407 isolates and
  3,106 species.
- **License / access:** Downloadable Zenodo datasets are CC BY 4.0 and include
  PDB, JSON, CSV, A3M, Foldseek, cluster, and network data. The web service and
  API were live when checked.
- **Confidence:** very high
- **Review note:** Added to `entries/viro3d.json`. Complements rather than
  duplicates VOGDB: Viro3D centers structure exploration, while VOGDB centers
  orthologous groups and annotation models.

### RNAVirHost

- **Kind:** command-line tool and machine-learning model
- **Purpose:** Predicts natural host groups for complete RNA-virus genomes
  using hierarchical classifiers, viral genomic traits, taxonomy, and sequence
  homology.
- **Source:** https://github.com/GreyGuoweiChen/VirHost
- **Publication:** https://doi.org/10.1093/gigascience/giae059
- **Version evidence:** Version 1.0.5 was uploaded to PyPI on 2024-05-25; paper
  published 2024-08-22. The repository was last pushed 2024-10-14.
- **License / language:** MIT; Python.
- **Installation:** Bioconda, PyPI, or source. It accepts genome FASTA input,
  includes an order-classification helper, and labels the evidence supporting
  each host result.
- **Confidence:** high
- **Review note:** Added to `entries/rnavirhost.json`. No equivalent dedicated
  RNA-virus host-prediction tool was found in the current catalog.

### The Plant Virus Transmissions Database

- **Kind:** curated web database
- **Purpose:** Connects more than 1,600 plant viruses to transmission modes,
  vectors, taxonomy, and evidence from over 3,500 publications dating to 1924.
- **Resource:** https://library.wur.nl/WebQuery/virus
- **Publication:** https://doi.org/10.1099/jgv.0.001957
- **RNA relevance:** Most represented plant viruses are RNA viruses, although
  the database is not restricted by genome type.
- **Publication date:** 2024-03-05.
- **License / access:** Freely searchable by virus, taxonomy, vector, and
  transmission mode. The paper is CC BY 4.0; no separate data license, bulk
  download, or API was found.
- **Confidence:** high for content; medium for data reuse rights
- **Review note:** Added to `entries/plant-virus-transmissions-database.json`.
  Display names and taxonomy are retained from source publications and may not
  match current ICTV names.

### AliMarko

- **Kind:** Snakemake pipeline
- **Purpose:** Aligns reads to a viral reference genome database and screens
  assembled contigs with profile HMMs, generating HTML reports with alignment,
  HMM match, and phylogenetic tree visualizations.
- **Source:** https://github.com/NJJeus/AliMarko
- **Version evidence:** README identifies v0.8; repository last pushed
  2025-10-17. No GitHub releases or tags exist.
- **License / language:** No license file found; Python.
- **Confidence:** medium; general virus detection rather than RNA-specific, and
  no license is declared.
- **Review note:** Added to `entries/alimarko.json` at the user's request, with
  `license` left null rather than inferred.

### Hecatomb

- **Kind:** Snakemake pipeline
- **Purpose:** Filters false-positive viral reads out of short- and long-read
  metagenomes to enrich true-positive viral sequences, with automated database
  and environment installation.
- **Source:** https://github.com/shandley/hecatomb
- **Publication:** https://doi.org/10.1093/gigascience/giae020
- **Version evidence:** PyPI/bioconda version 1.3.4, uploaded 2025-09-16.
- **License / language:** MIT; Python.
- **Confidence:** high; general viral metagenomics rather than RNA-specific.
- **Review note:** Added to `entries/hecatomb.json`.

### RolyPoly

- **Kind:** command-line toolkit and Python library
- **Purpose:** RNA virus analysis toolkit spanning read filtering, assembly,
  RdRp/nucleotide marker search, ICTV taxonomy assignment, RNA structure and
  ribozyme annotation, and contig binning.
- **Source:** https://github.com/UriNeri/rolypoly
- **Package:** https://pypi.org/project/rolypoly-tk/
- **Version evidence:** PyPI version 0.7.18; latest GitHub release v0.7.18
  published 2026-08-20. Still pre-v1 with a manuscript planned for late 2026.
- **License / language:** GPL-3.0; Python.
- **Confidence:** high; explicitly RNA-virus-focused and actively maintained.
- **Review note:** Added to `entries/rolypoly.json` with `doi` left null since
  no dedicated software paper exists yet.

### Virusparies

- **Kind:** R package
- **Purpose:** Imports, filters, and plots VirusHunterGatherer hittables,
  producing boxplots, scatterplots, bar plots, violin plots, and graphical
  summary tables annotated with ICTV taxonomy.
- **Source:** https://github.com/SergejRuff/Virusparies
- **Version evidence:** GitHub/CRAN release v1.0.0, published 2024-11-15.
- **License / language:** GPL-3.0; R.
- **Confidence:** high; direct companion to VirusHunterGatherer.
- **Review note:** Added to `entries/virusparies.json` with `doi` left null
  since no dedicated software paper was found.

### VirusHunterGatherer

- **Kind:** Snakemake pipeline
- **Purpose:** Two-stage virus discovery workflow: profile HMM-based homology
  search for viral reads (Virushunter) followed by seed-based iterative genome
  assembly (Virusgatherer); ships with a dedicated RNA virus pHMM profile set.
- **Source:** https://github.com/lauberlab/VirusHunterGatherer
- **Version evidence:** GitHub release v1.0.0, published 2026-08-11.
- **License / language:** GPLv3 per README (GitHub API license field was
  empty); Perl.
- **Confidence:** high; general virus discovery workflow with an RNA-specific
  profile set, and the primary source for Virusparies' outputs.
- **Review note:** Added to `entries/virushuntergatherer.json` with `doi` left
  null; the README explicitly notes a pipeline citation is still pending.

### Rfam Viral RNA Families

- **Kind:** database (Rfam project subset)
- **Purpose:** Curated collection of covariance models and structure
  annotations for conserved viral RNA elements, including complete
  Coronaviridae, Hepacivirus, and Flaviviridae 5'/3' UTR families generated
  with R2DT.
- **Resource:** https://rfam.org/viruses
- **Publication (preprint):** https://doi.org/10.64898/2026.05.10.724034
- **Version evidence:** Current families were added across Rfam releases 14.2
  through 15.1; the project is ongoing with Filoviridae and Rhabdoviridae
  families in progress.
- **License / access:** CC0 1.0 (Rfam-wide license); web browsing, downloads,
  and API access.
- **Confidence:** high; explicitly RNA-structure-focused viral resource.
- **Review note:** Added to `entries/rfam-viral-rna-families.json`, using the
  companion preprint date for `date` and leaving `data_updated` null pending a
  specific release date for the viral family set.

### VirBot

- **Kind:** command-line tool
- **Status:** Already present in the catalog as
  `entries/virbot-an-rna-viral-contig-detector-for-metagenomic-data_2023.json`,
  which links directly to https://github.com/GreyGuoweiChen/VirBot. No new
  entry was created.

## Not Included (for now)

### The Zoe Anthology

- **Kind:** Rust library
- **Purpose:** Implements sequence formats, alignments, transformations,
  validation, distances, k-mer operations, and search algorithms for viral
  genomics, with emphasis on methods used in RNA-virus sequencing.
- **Source:** https://github.com/CDCgov/zoe
- **Documentation:** https://cdcgov.github.io/zoe/
- **Package:** https://crates.io/crates/zoe
- **Version evidence:** Crate first released 2025-05-09; version 0.0.31 released
  2026-07-15, with repository activity through 2026-08-25.
- **License / language:** Apache-2.0; Rust.
- **Installation:** `cargo add zoe`. The current release requires nightly Rust
  and declares Rust 1.95.
- **Confidence:** high
- **Decision:** Held out at the user's request for now. It is valid and
  actively maintained, but it is a programming library rather than a
  standalone analysis workflow, and no peer-reviewed Zoe publication was found.

### Phyrvm

- **Kind:** command-line pipeline
- **Purpose:** Runs RNA-virus discovery, phylogenetic analysis, characterization,
  and phylogeny-based host-association prediction from sequencing reads.
- **Source:** https://github.com/ZiyueYang01/Phyrvm
- **Package:** https://pypi.org/project/phyrvm/
- **Version evidence:** PyPI version 1.1.0 was uploaded 2024-06-18; repository
  last pushed 2024-06-21. There are no GitHub tags or releases.
- **License / language:** MIT; Python and R.
- **Installation:** PyPI plus numerous Conda tools, R packages, and large local
  rRNA, taxonomy, NR, and NT resources.
- **Confidence:** medium
- **Decision:** Held out at the user's request for now, as the project appears
  orphaned: no indexed paper was found, and release discipline and recent
  maintenance are limited.

## Hold

### RNA Viral Protein Structure Database (RVPSD)

- **Kind:** RNA-virus-specific web database
- **Purpose:** Integrates taxonomy, sequences, functional annotations, and
  154,716 predicted protein structures from 5,263 RNA-virus species.
- **Resource:** https://virus.9itsg.net/
- **Publication:** https://doi.org/10.1002/imo2.70120
- **Publication date:** 2026-07-13.
- **License / access:** The paper is CC BY 4.0. No database-specific license,
  bulk download, API, or public source repository was verified.
- **Confidence:** medium-high for the publication; medium for operations
- **Hold reason:** The service responded but presented an expired TLS
  certificate when checked on 2026-08-31. Recheck service health and reuse terms
  before promotion.

### VIP-DB

- **Kind:** evidence-guided web database
- **Purpose:** Links plant viruses, insect vectors, host plants, transmission
  modes, taxonomy, and traceable publications in 1,375 integrated records.
- **Resource:** https://viplant.cn/#/
- **Publication:** https://doi.org/10.3390/v18060679
- **RNA relevance:** The paper reports 170 ssRNA and 13 dsRNA virus species,
  alongside DNA viruses and a small number of other or unclassified viruses.
- **Publication date:** 2026-06-18.
- **License / access:** The paper and supplementary relationship table are CC
  BY 4.0. No separate database license or API was identified.
- **Confidence:** high for content; medium for operations and reuse terms
- **Hold reason:** The site required bypassing an expired TLS certificate when
  checked on 2026-08-31. It is not a duplicate of the WUR resource: VIP-DB is
  insect-centered and models evidence-traceable virus-insect-plant triples.

## Search Record

Primary-source searches used combinations of:

- `RNA virus software 2025 GitHub DOI`
- `RNA virus database 2025 2026 resource`
- `metatranscriptomic RNA virus pipeline 2025`
- `segmented RNA virus software co-occurrence`
- `RdRp profile HMM software database 2025 2026`
- `RNA virus endogenous viral element Nextflow`
- Exact candidate names and publication DOIs on GitHub, Crossref, OpenAlex,
  Europe PMC, PyPI, Zenodo, Figshare, and project release pages.

Other leads rejected during this pass were CATCH applications and nanopore
adaptive-sampling papers that used existing methods but did not release a
distinct reusable RNA-virus software package. IMG/VR v4 was also rejected as a
"new" database because its canonical publication predates this search window;
MetaVR is its newer successor and is documented separately above.