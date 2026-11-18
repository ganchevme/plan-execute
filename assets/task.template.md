# Task title

ID: CORE-01
Status: todo
Dependencies: none
Type: red / green / red+green / setup / validation / documentation / design
Owner: orchestrator assigns one bounded worker
Verification: not run
Blocker: none

## Inputs

Required: name exact contract sections, source interfaces and prerequisite evidence needed for this task.

Conditional: link other references with a short description and a trigger for reading each. Do not require the whole testing guide, every plan/task or unrelated historical logs. Relevant earlier logs may be read when useful for diagnosis or review. The project guide holds essential constraints and routes to shared execution/handoff procedures; reference those rather than copying them into this task.

## Owned scope

List files or boundaries the worker may change, exclusions and coordination needs. Identify local decisions the worker may make; unresolved decisions affecting shared behavior or dependent work must be settled before implementation or covered by a prerequisite investigation/design task. Omit empty decision lists.

## Work

Specify a bounded observable outcome; no speculative follow-on features. Distinguish required behavior from suggested implementation. Keep shared contracts in their canonical location and link them here. Where consequential commitments need explanation, include or link their supporting use case, known origin and practical tradeoff; omit routine decision bookkeeping.

## Acceptance and verification

State behavioral assertions, precise commands and environment setup prerequisites. Where reasonable implementations could differ, give a concrete example or invariant, including boundary/failure behavior when it clarifies acceptance. Choose evidence that can detect the relevant failure and supports any environment-specific claim; avoid exhaustive checklists. RED must reach an intended failing assertion before implementation; GREEN preserves accepted tests and passes prescribed checks. A combined task requires both RED evidence and passing GREEN verification before completion. Other task types use appropriate evidence. Keep default checks synthetic. Name the focused test command and relevant testing-guide section; do not copy the entire testing policy. Request concise counts, exit status and assertion evidence first, with the fresh raw-log path for deeper diagnosis.

## Evidence

Record concise task-specific changes, command/exit evidence, relevant behavioral assertions, fresh log paths and blockers as work proceeds. Follow the shared project protocol for assignment, review, status, logging and commits. Keep transient worker briefs, copied generic handoff instructions, raw logs and secrets out of this record.
