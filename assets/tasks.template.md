# Task register

Use this exact table schema for validator support, one complete task row per line. Initialize this file only when the register is missing; otherwise add rows to the existing register, preserving IDs, statuses and evidence. Replace the example before delivering. Paths are relative to this file. List every executable task here; keep detailed evidence and blockers in task files. Update the matching row by stable ID and synchronize its task-file status. Do not duplicate this table in the project guide or component guides.

Retrieve exact ID/status rows with targeted, batched searches when useful. For broad review or a small register, a full read may be cheaper. Check global consistency with an available plan validator and a permitted Python 3.9+ interpreter. Otherwise review IDs, task links, statuses, dependencies and cycles manually and disclose that automated validation was not run. If the user or project explicitly requires the automated check, unavailable tooling is a blocker.

| ID | Task | Status | Dependencies | File |
|---|---|---|---|---|
| CORE-01 | Example task | todo | none | [Task](tasks/CORE-01.md) |
