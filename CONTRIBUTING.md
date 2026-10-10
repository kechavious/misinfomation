# Contributing

Install the pinned dependencies and editable package as shown in the README.
Run `python -m unittest discover -s tests -v` and a small CLI experiment before
submitting a change. Keep simulation rules in `simulations/`, not duplicated in
notebooks. Document any model changes and regenerate results with explicit
parameters and seeds. Historical versions are preserved in Git; see `docs/history.md`.

Avoid committing virtual environments, credentials or temporary outputs. Include
behavioral tests for changes to transmission, timing, threshold definitions and
uncertainty. Distinguish model assumptions from empirical conclusions.

Edit `reports/paper.md.in` for report changes, then run
`bash scripts/build_paper.sh`. Run `python scripts/generate_paper.py --check`
to ensure the Markdown agrees with the template and reference data. Review the
PDF layout before committing it.
