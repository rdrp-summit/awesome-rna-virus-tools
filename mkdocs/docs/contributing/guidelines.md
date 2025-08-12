# Contributing Guidelines

Thank you for your interest in contributing to the Awesome RNA Virus Tools collection! This guide will help you understand how to add new tools, improve existing entries, and contribute to the community.

## 🚀 Quick Start

### Adding a New Tool

1. **Fork the repository** on GitHub
2. **Create a new JSON file** in the `entries/` directory
3. **Follow the schema** defined in `scripts/schema.json`
4. **Test your entry** by running the validation scripts
5. **Submit a pull request** with your changes

### Example Entry

```json
{
  "name": "YourToolName",
  "url": "https://github.com/username/your-tool",
  "doi": "10.1000/example.doi",
  "description": "Brief description of what your tool does",
  "date": "2025-01-15",
  "version": "1.0.0",
  "license": "MIT",
  "language": "Python",
  "topics": ["rna-virus-identification", "metagenomics"],
  "package_managers": ["pip", "conda"],
  "platforms": ["linux", "macos", "windows"],
  "installation_methods": ["source", "binary"]
}
```

## 📋 Entry Requirements

### Required Fields
- **name**: Tool name
- **url**: Homepage or repository URL
- **description**: Clear, concise description (1-2 sentences)
- **topics**: At least one topic from the approved list

### Recommended Fields
- **doi**: Publication DOI if available
- **license**: Software license
- **language**: Primary programming language
- **package_managers**: Installation methods (pip, conda, etc.)
- **platforms**: Supported operating systems
- **version**: Latest version number
- **date**: Publication or release date

### Optional Fields
- **bibtex**: Full citation in BibTeX format
- **input_formats**: Supported input file formats
- **output_formats**: Generated output formats
- **installation_methods**: Installation approaches

## 🏷️ Topic Categories

Use these standardized topics to categorize your tool:

- **rna-virus-identification**: General RNA virus detection
- **rdrp-detection**: RdRp-specific detection tools
- **genome-assembly**: Viral genome assembly
- **annotation**: Genome annotation and gene prediction
- **phylogenetics**: Phylogenetic analysis tools
- **host-prediction**: Host-virus interaction prediction
- **databases**: Sequence databases and resources

## 🔍 Quality Standards

### Tool Inclusion Criteria

✅ **Include tools that:**
- Are actively maintained or widely used
- Have clear documentation
- Are relevant to RNA virus research
- Are publicly available
- Have been published or are in preprint

❌ **Avoid tools that:**
- Are no longer maintained (unless historically significant)
- Lack documentation
- Are proprietary without academic access
- Are duplicates of existing entries
- Are too general (not virus-specific)

### Description Guidelines

- **Be concise**: 1-2 sentences maximum
- **Be specific**: Mention key features or use cases
- **Avoid jargon**: Use accessible language
- **Include context**: Mention the type of analysis or data

**Good examples:**
- "Deep learning method for identifying viral sequences from metagenomic data"
- "Specialized assembler for coronavirus genomes with improved handling of repetitive regions"

**Avoid:**
- "Great tool for virus stuff"
- "The best assembler ever made"
- "Tool that does many things"

## 🛠️ Development Workflow

### Local Testing

1. **Install dependencies:**
   ```bash
   pip install -r mkdocs/requirements.txt
   ```

2. **Validate your entry:**
   ```bash
   python scripts/validate_entries.py
   ```

3. **Generate documentation:**
   ```bash
   python scripts/update_docs.py
   ```

4. **Test the site locally:**
   ```bash
   cd mkdocs && mkdocs serve
   ```

### File Naming

- Use lowercase with hyphens: `tool-name.json`
- Match the tool name: `virsorter2.json`
- Avoid spaces and special characters

### JSON Formatting

- Use 2-space indentation
- Sort fields alphabetically (optional but preferred)
- Validate JSON syntax before submitting

## 📝 Pull Request Process

### Before Submitting

- [ ] Entry follows the schema requirements
- [ ] JSON is valid and properly formatted
- [ ] Tool meets inclusion criteria
- [ ] Description is clear and concise
- [ ] All URLs are accessible
- [ ] Entry has been tested locally

### PR Template

When submitting a pull request, please include:

```markdown
## Tool Addition: [Tool Name]

### Description
Brief description of the tool and its purpose.

### Checklist
- [ ] Entry follows schema requirements
- [ ] JSON is valid
- [ ] Tool is actively maintained
- [ ] Documentation is available
- [ ] Tested locally

### Additional Notes
Any additional context or special considerations.
```

## 🔄 Maintenance

### Updating Existing Entries

- **Version updates**: Update version numbers and dates
- **URL changes**: Fix broken or redirected links
- **Metadata improvements**: Add missing fields
- **Description refinements**: Improve clarity

### Reporting Issues

Use GitHub Issues to report:
- Broken links
- Outdated information
- Missing tools
- Schema improvements
- Website bugs

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

- **Be respectful**: Treat all contributors with respect
- **Be constructive**: Provide helpful feedback
- **Be collaborative**: Work together to improve the resource
- **Be patient**: Remember that everyone is learning

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Slack**: Real-time community chat
- **Email**: Direct contact for sensitive issues

## 🏆 Recognition

### Contributors

All contributors are recognized in:
- Repository contributor list
- Annual community reports
- Conference presentations
- Academic publications (when appropriate)

### Maintainers

Active contributors may be invited to join the maintenance team with:
- Commit access to the repository
- Participation in project decisions
- Recognition as a core maintainer

## 📚 Resources

### Helpful Links

- [JSON Schema Documentation](https://json-schema.org/)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Markdown Guide](https://www.markdownguide.org/)

### Tools for Contributors

- [JSONLint](https://jsonlint.com/): Validate JSON syntax
- [Schema Validator](https://www.jsonschemavalidator.net/): Test against schema
- [Markdown Editor](https://dillinger.io/): Preview markdown formatting

## ❓ Getting Help

### Common Issues

**Q: My JSON file won't validate**
A: Check for trailing commas, missing quotes, and proper nesting

**Q: How do I choose the right topics?**
A: Select 1-3 topics that best describe the tool's primary functions

**Q: Can I add a tool that's not published yet?**
A: Yes, if it's publicly available and has documentation

**Q: What if a tool fits multiple categories?**
A: Use multiple topics, but prioritize the most relevant ones

### Contact

- **General questions**: [GitHub Discussions](https://github.com/rdrp-summit/awesome-rna-virus-tools/discussions)
- **Technical issues**: [GitHub Issues](https://github.com/rdrp-summit/awesome-rna-virus-tools/issues)
- **Direct contact**: [contact@rdrp-summit.org](mailto:contact@rdrp-summit.org)

---

Thank you for helping to build the most comprehensive resource for RNA virus research tools! 🦠🔬