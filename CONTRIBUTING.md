# Contributing to Awesome RNA Virus Tools

Contributions are made through pull requests. You can add software, a database,
or a literature record by creating one JSON file in `entries/`.

## Add an entry

1. Fork the repository and create a focused branch.
2. Copy a nearby entry of the same `type`: `tool`, `database`, or `paper`.
3. Give the file a lowercase, hyphenated name and complete its metadata.
4. Run `npm install` once, then `npm run build` before opening the pull request.
5. Explain the entry's relevance to RNA virus research in the pull request.

Astro validates every entry while building. A pull request cannot merge cleanly
if required fields are missing or have incompatible types.

## Entry requirements

Every entry needs `name`, `title`, `url`, `description`, at least one `topic`,
and a valid `type`. Include a DOI and software metadata when they are available.
Descriptions should be concise, factual, and free of promotional claims.

For workflow tools, use `workflow_managers` with values such as `Nextflow`,
`Snakemake`, or `WDL`. Installation channels belong in `package_managers`, and
user-facing modes such as `CLI` or `Web Interface` belong in `interface`.

Corrections to existing metadata use the same workflow. For a lightweight
suggestion without a prepared JSON file, open a new-entry issue instead.
