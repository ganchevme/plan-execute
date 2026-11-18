# Project guide

Use this template when the shared project guide is missing; otherwise update only affected scope, policy or routing. Keep this guide self-contained. Put substantial project-specific procedures in linked project files; generated plans must not depend on an installed skill path.

## Goal and boundaries

Describe the intended outcome, non-goals and essential safety/authorization boundaries every executor must know. Planning does not start implementation.

## Resolved execution preferences

Record a compact resolved policy once, with provenance: model roles, exclusions, ordinary/demanding effort, worker effort ceiling and routing, isolation/runtime, logging/wrapper, TDD, parallelism and commits. Preserve it on resume; changed personal defaults do not alter this project. Announce the local per-task commit default and opt-out when first resolved. Task evidence records material model selections, escalations or deviations, and reported values needed to establish exact-model/effort requirements. Do not repeat unchanged policy or claim inherited/unreported settings were verified. No credentials.

## Working protocol

Plan-only work ends at handoff. Explain material tradeoffs before changing commitments. Execute/resume only the authorized scope: inspect current changes/evidence, select tasks with completed prerequisites and settled shared decisions, and continue through the requested batch or report concrete blockers.

Delegate bounded work by default; keep tiny or context-heavy work local when transfer costs more. Give workers scope, required inputs and checks. Use one owner per editable file; parallel work needs ready dependencies and settled interfaces. The orchestrator owns integration, acceptance, shared status and commits. Enforce resolved model restrictions and the worker effort ceiling for both ordinary and demanding work, including escalations. When inherited effort cannot be established within the ceiling, select an explicit supported level within it. Report unsupported requirements without silent substitution or claiming compliance.

Review acceptance criteria, actual changes including new/untracked files, and evidence tied to those changes. Tests are synthetic by default; live checks need authorization. With TDD enabled for new behavior, the planner chooses RED/GREEN phases within one task or separate tasks, considering scope, ownership, dependencies and the value of independent acceptance or a handoff. Prove the intended assertion failure before implementation and preserve accepted tests. A combined task completes only after GREEN passes; a separate RED task completes on intended failing-assertion evidence, then GREEN depends on it. Setup/docs/existing behavior need no artificial RED; explicit task contracts remain binding unless deliberately revised.

Record concise evidence in task files and synchronize TASKS.md statuses. Update this guide only when scope, policy, preferences or routing change. Append log entries in append mode; relevant older logs may be read. Use an available permitted wrapper or direct capture without automatic installation. Commit accepted task changes/status only when enabled, before the next sequential task. No implied repository creation, push or history rewriting.

## File map

Adapt these entries to files actually present. Give each reference a purpose and read condition; read only relevant task inputs and triggered references, using targeted register/dependency lookups when useful.

| File | Purpose | Read when |
|---|---|---|
| [TASKS.md](TASKS.md) | Compact task register: IDs, status, dependencies and task links | Selecting work or checking/updating relevant rows |
| tasks/<id>.md | Owned scope, exact inputs, acceptance and current verification | Executing or reviewing that task |
| [TESTING.md](TESTING.md) | Test commands, setup and verification procedures | The selected task requires a named section or troubleshooting needs it |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Component ownership and design decisions | A task touches those boundaries or a design review needs them |
| [CONTRACTS.md](CONTRACTS.md) | Public interfaces and shared data/error contracts | Implementing or reviewing the affected contract sections |

Keep verified observations, assumptions, reuse/adapt/build findings and open decisions in the relevant design/reference file when substantial. This guide changes with scope, policy, preferences or routing, and contains no task table or changing progress totals.
