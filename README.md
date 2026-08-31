# Awesome RNA Virus Tools

<img src="rdrp_summit.png" alt="RdRp Summit" width="160">

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Frdrp-summit.github.io%2Fawesome-rna-virus-tools%2F)](https://rdrp-summit.github.io/awesome-rna-virus-tools/)
[![License](https://img.shields.io/github/license/rdrp-summit/awesome-rna-virus-tools)](LICENSE)

A community-curated catalog of software, databases, and literature for RNA virus
research. Use the [interactive catalog](https://rdrp-summit.github.io/awesome-rna-virus-tools/)
to search by name, topic, description, language, or interface.

## Catalog structure

- **Software** is the primary collection and includes analysis tools and workflows.
- **Databases** are practical data resources shown alongside software.
- **Literature** has a separate explorer view for papers, reviews, and methods.

Each record is a reviewable JSON file in `entries/`. Astro loads and validates
those records directly, then generates the static site and entry detail pages.

## Local development

Requires Node.js 22 or newer.

```bash
npm install
npm run dev
```

Open `http://localhost:4321/awesome-rna-virus-tools/`.

Run the same check used by pull requests before submitting a change:

```bash
npm run build
```

Pixi users can run `pixi run site-dev` and `pixi run site-build` instead.

## Contributing

Pull requests remain the preferred way to add or correct entries. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the entry requirements and workflow.
Lightweight suggestions can also be submitted through the new-entry issue form.

## Data and validation

The JSON files in `entries/` are the catalog's source of truth. Astro validates
their shape and generates the site directly; generated pages are not committed.

This project builds on the work of
[awesome-virome](https://github.com/shandley/awesome-virome).