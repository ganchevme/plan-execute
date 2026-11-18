---
name: plan-execute
description: Plan software projects and execute or resume their implementation through bounded tasks, delegated workers, verification and review. Use for project planning, task decomposition, revising plans, implementing selected tasks or batches, and continuing work under an existing plan. Not for unrelated one-off edits or implementation implied only by a planning request.
license: MIT
metadata:
  version: "0.1.0"
---

# Plan & Execute

Turn project intent into an executable plan, then carry authorized work through implementation, verification and review. Keep the project’s durable state in files so a fresh session can continue without reconstructing conversation history. Planning alone does not authorize implementation, live data transfer, external messages or deployment.

## Route by the user's intent

- **Plan:** initialize project planning, extend an existing task register or revise affected architecture, contracts and tasks. Read [references/planning.md](references/planning.md). Do not start implementation unless requested.
- **Execute:** implement a selected task, the next ready task or an authorized batch. Read [references/execution.md](references/execution.md) and follow its execution loop; do not repeat planning research when the plan already settles the question.
- **Resume:** continue the previously authorized scope through execution mode. Inspect current task state, working changes and concise verification before choosing where to restart. A bare “continue” after a planning-only exchange continues planning, not implementation.
- **Plan and implement:** perform the necessary planning, then execute the requested scope without asking again for permission already given.

If the intended outcome or scope is materially ambiguous, clarify that point while continuing independent inspection. Never treat the skill’s invocation alone as authority to execute the entire backlog.

Planning mode covers consequential choices and complexity review. Execution mode owns the task lifecycle, worker protocol, verification, logging and commit procedures; settings mode defines model and environment preferences.

## Shared project context

Read applicable project instructions and `plan/PROJECT.md`, then relevant `plan/TASKS.md` rows, the selected task and its required inputs. PROJECT.md holds stable goals, boundaries, resolved preferences and routing. TASKS.md is the compact register; task files hold scope, acceptance and current evidence. Do not create or overwrite AGENTS.md.

Minimize context and tool round trips. Use `rg` to match whole ID/status columns and batch dependency lookups; substring matches may select another task or a dependency. Read the full register when small enough or broad review makes that cheaper. Read conditional references only when their trigger applies; avoid reloading unchanged files or entire testing guides. Read relevant current or earlier logs when useful, preferring excerpts over unrelated history.

Extend initialized plans in place, reusing shared contracts, procedures and resolved preferences. Planning mode defines how to add or revise work without recreating setup or duplicating procedures.

For initialization, requested preference changes or missing required settings, read [references/settings.md](references/settings.md). Later work uses the frozen policy in PROJECT.md; explicit user instructions and applicable project rules remain authoritative. Preserve unrelated work and never record secrets.

The supported layout uses PROJECT.md plus TASKS.md. If a requested existing plan uses another layout, report the mismatch and preserve its files and progress; restructure it only when requested.

## Completion

Planning returns the guide/register links, important decisions and unresolved blockers. Execution returns completed task IDs, concise verification, local commit hashes when enabled, and remaining blockers or unfinished requested work. Continue through the authorized batch, stopping for scope completion or a concrete blocker; never claim completion solely from a worker’s report.
