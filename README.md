# Awesome RNA Virus Tools

![RdRp Summit Logo](assets/awesome-rna-virus-tools-hex.png)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Website](https://img.shields.io/website?url=https%3A//rdrp-summit.github.io/awesome-rna-virus-tools/)](https://rdrp-summit.github.io/awesome-rna-virus-tools/)
[![GitHub](https://img.shields.io/github/license/rdrp-summit/awesome-rna-virus-tools)](LICENSE)

A curated list of software, tools, databases and resources for RNA virus analysis, prediction, annotation, phylogenetics, and related research. This project builds upon the excellent [awesome-virome](https://github.com/shandley/awesome-virome) list.

🌐 **[Visit the interactive website](https://rdrp-summit.github.io/awesome-rna-virus-tools/)** to explore tools by categories, programming languages, and installation methods.

## Quick Navigation

- [RNA Virus Identification](#rna-virus-identification)
- [RdRp Detection](#rdrp-detection)
- [Genome Assembly](#genome-assembly)
- [Phylogenetics](#phylogenetics)
- [Contributing](#contributing)

## RNA Virus Identification

Tools for detecting and identifying RNA viruses in sequencing data.

- **[palmID](https://github.com/rcedgar/palmscan)** - Identifies and classifies RNA virus sequences based on the conserved RdRp palm domain (Language: C++, License: GPL-3.0, Install: github, Platforms: linux, macos, windows, Methods: source, binary, DOI: [10.1093/ve/veab050](https://doi.org/10.1093/ve/veab050))
- **[RdRp-scan](https://github.com/JustineCharon/RdRp-scan/)** - Fast profile-based detection of RNA-dependent RNA polymerase (RdRp) sequences for exploring the 'dusk matter' of the RNA virosphere (Language: Python, Install: bioconda)
- **[Serratus](https://github.com/ababaian/serratus)** - Ultra-high throughput discovery of RNA viruses from public sequencing data using cloud computing (Language: Python, License: GPL-3.0, Install: bioconda, DOI: [10.1038/s41586-021-04332-2](https://doi.org/10.1038/s41586-021-04332-2))

## RdRp Detection

Specialized tools for detecting RNA-dependent RNA polymerase sequences.

- **[palmID](https://github.com/rcedgar/palmscan)** - Identifies and classifies RNA virus sequences based on the conserved RdRp palm domain (Language: C++, License: GPL-3.0, Install: github, Platforms: linux, macos, windows, Methods: source, binary, DOI: [10.1093/ve/veab050](https://doi.org/10.1093/ve/veab050))
- **[RdRp-scan](https://github.com/JustineCharon/RdRp-scan/)** - Fast profile-based detection of RNA-dependent RNA polymerase (RdRp) sequences for exploring the 'dusk matter' of the RNA virosphere (Language: Python, Install: bioconda)

## Genome Assembly

Tools for assembling viral genomes from sequencing data.

- **[coronaSPAdes](https://github.com/ablab/spades)** - Specialized assembler for coronavirus genomes and other RNA viral sequences (Language: C++, License: GPL-2.0, Install: bioconda, DOI: [10.1093/bioinformatics/btab597](https://doi.org/10.1093/bioinformatics/btab597))
- **[metaviralSPAdes-RNA](https://github.com/ablab/spades)** - Modified metaSPAdes assembler optimized for RNA viral genome assembly from metagenomic data (Language: C++, License: GPL-2.0, Install: bioconda, DOI: [10.1093/bioinformatics/btab102](https://doi.org/10.1093/bioinformatics/btab102))

## Phylogenetics

Tools for phylogenetic analysis and evolutionary studies of RNA viruses.

- **[ViralMSA](https://github.com/niemasd/ViralMSA)** - Massively scalable reference-guided multiple sequence alignment of viral genomes, including RNA viruses (Language: Python, License: GPL-3.0, Install: bioconda, DOI: [10.1093/bioinformatics/btaa743](https://doi.org/10.1093/bioinformatics/btaa743))



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

*Last updated: 2025-08-14 16:57:13 UTC*
