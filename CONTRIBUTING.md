# Contributing

Install the pinned dependencies and editable package as shown in the README.
Run `python -m unittest discover -s tests -v` and a small CLI experiment before
submitting a change. Keep simulation rules in `simulations/`, not duplicated in
notebooks. Document any model changes and regenerate results with explicit
parameters and seeds. Preserve historical artifacts in `docs/archive/`.

Avoid committing virtual environments, credentials or temporary outputs. Include
behavioral tests for changes to transmission, timing, threshold definitions and
uncertainty. Distinguish model assumptions from empirical conclusions.
