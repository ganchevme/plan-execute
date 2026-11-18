# Contributing

This skill is maintained primarily for my own use. Keeping it lean, understandable and dependable is a priority.

Forks, copies and adaptations are welcome under the project's license.

Contributions are considered selectively. Small bug fixes and precise clarifications are the most likely to be accepted. Explain the concrete problem, provide a reproducible example where applicable, and justify why the proposed change is necessary and narrowly scoped.

For a correction beyond a small fix, open an issue to discuss it before preparing a pull request.

Feature requests, broad refactoring and additional dependencies are generally outside the project's scope.

Contributors must understand, review and verify everything they submit, including AI-generated material. Unexplained or unverified changes are unlikely to be reviewed.

There is no commitment to review or merge submissions.

## Verification

Use a suitable Python 3.9+ interpreter in this repository's permitted development environment; these checks require no third-party Python packages. This example creates a local environment named `.venv` from the checkout root; use equivalent commands for an existing environment or another interpreter name/location:

```sh
python3 -m venv .venv
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
.venv/bin/python scripts/check_package.py
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. Include the relevant command results with your proposal. For instruction changes, explain the realistic scenario you checked and the observed behavior.
