# Research report source

The current report is published as [`docs/paper.md`](../docs/paper.md) and
[`docs/paper.pdf`](../docs/paper.pdf). Edit `paper.md.in` rather than the generated
Markdown. Tables and numerical fields come from the checked-in reference CSVs.

## Build

Activate the project Python environment. Install Pandoc and a pdfLaTeX distribution
with the standard `article`, `geometry`, `booktabs`, `longtable`, `hyperref`, and
`xcolor` packages. The tested tools are Pandoc 3.1.11.1 and TeX Live 2025.
On Debian/Ubuntu, `pandoc`, `texlive-latex-recommended` and
`texlive-latex-extra` supply the relevant tools and packages.

From the repository root:

```bash
bash scripts/build_paper.sh
```

To regenerate or check only the Markdown without installing a TeX toolchain:

```bash
python scripts/generate_paper.py
python scripts/generate_paper.py --check
```

The generator verifies the CSV hashes, seven configurations, experiment
parameters, graph counts and trial-group sizes. It refuses to reuse the current
interpretation for a changed experiment design. If changing the model or
reference parameters, update the report's assumptions and interpretation as
well as regenerating the experiment outputs.

The PDF uses the same generated Markdown. Rebuild it after editing the template;
review page layout and tables before committing. The build does not run any
simulation or fetch external references. PDF bytes can differ between builds due
to timestamps and typesetting environment.
