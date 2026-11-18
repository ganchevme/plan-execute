# Planning mode

Use for initializing, extending or revising a plan. Plan-only requests end with the handoff; a request to plan and implement continues into execution within the authorized scope.

## Initialize, extend or revise

Inspect existing project planning before creating infrastructure:

- **Initialize:** when shared planning is absent, create the minimum guide, register, task records and useful references. Resolve settings using [settings.md](settings.md), record effective values and provenance in PROJECT.md, and announce the local per-task commit preference once.
- **Extend:** for additional work in an initialized project, inherit applicable procedures, contracts and frozen preferences. Add task files and rows to the existing register, preserving IDs, statuses and evidence. Create feature-specific design material only when substantial decisions need it; reference shared procedures instead of copying them. Fill missing required pieces without recreating existing setup or re-announcing settled preferences.
- **Revise:** when new scope changes shared behavior, update the affected canonical contracts, task dependencies and guidance together. Edit PROJECT.md only for changes to scope, policy, preferences or routing. Preserve unrelated work and completed-task evidence; add adaptation tasks where completed implementations need changes.

Follow the supported-layout rule in [SKILL.md](../SKILL.md). Additional work alone does not require a second project guide, register or execution protocol.

## Explore before deciding to build

Establish outcomes, non-goals, data ownership, side effects, failure behavior and what the user decides manually. Inspect the repository and available tooling. Before decomposing custom implementation, assess existing libraries, frameworks, products and internal components. Research current candidates when needed; compare fit, maintenance, licensing, privacy, deployment and integration cost. Give a bounded reuse/adapt/build recommendation rather than an exhaustive catalog. Ask when tradeoffs affect the user's outcome, not for every dependency choice.

When a question could materially increase scope or complexity, explain the concrete capability, added implementation/operating work and a simpler viable option before asking. Recommend an option based on the known use case and make the tradeoff understandable without specialist knowledge. Prefer asking whether other teams must install integrations without changing or redeploying the application over asking whether it should be "extensible." Resolve routine implementation choices locally; do not turn every choice into a questionnaire.

For consequential commitments, keep a brief supporting use case, origin (explicit request, agent proposal accepted by the user, or assumption) and discussed tradeoff in the relevant canonical decision/task record. Preserve known context without inventing missing history; mark unknown rationale as unknown. Record only what aids later decisions, not a provenance ledger for every preference.

Identify assumptions whose failure would change the plan. Verify these with documentation, source inspection or small authorized probes, preferably synthetic/read-only. Preserve privacy and existing authorization boundaries. Distinguish observations, assumptions and unverified behavior; one successful request is not proof of all capabilities. Record useful findings, not raw private data.

## Define contracts before implementation tasks

Separate reusable capability from application policy when reuse is desired. Specify public inputs, outputs, errors, dependencies, configuration ownership and persistence. Reusable components must not import application-specific policy or discover its credentials implicitly. If copyable/standalone packaging is a requirement, include isolated installation and resource tests.

When initializing, use `plan/PROJECT.md` as a short, stable entry point: objective, essential safety boundaries, compact resolved preferences, a self-contained working protocol and a file map with descriptions and explicit read conditions. Generated plans must remain usable without this skill installed; link substantial project procedures from project-owned files, never a machine-specific skill path. Reuse this entry point for extensions. Keep task rows, changing progress summaries, detailed contracts and feature-specific test coverage out of the guide. Use `plan/TASKS.md` for the compact register and separate task files for bounded work and evidence. Link testing procedures and substantial architecture/contracts as needed; do not create empty reference files or require every reference on every turn. Large projects first establish shared architecture, interfaces and component milestones; then plan components against those contracts. Read [large-projects.md](large-projects.md) only for hierarchical planning. Do not detail distant uncertain work merely to fill a backlog.

## Produce executable tasks

Use the templates in assets as contracts, adapting their explanatory text. Every executable task has a globally unique ID, status, dependencies, owned scope/files, named inputs, bounded work, acceptance criteria and verification. The task register lists every executable task and its status, one task per line. Keep component milestones separate from executable tasks. Use `../assets/project.template.md` and `../assets/tasks.template.md` only for missing shared records; use `../assets/task.template.md` for new tasks. Keep generic execution, delegation, logging and handoff procedures in canonical shared guidance; tasks link relevant procedures and contain only task-specific details or necessary exceptions.

Size tasks for one focused worker and a meaningful review; split when ownership, prerequisite interfaces or verification become unclear. Preserve stable IDs when inserting tasks. Dependency order is authoritative, not numeric order. Parallelize only ready work with settled interfaces and disjoint ownership; use isolated worktrees when appropriate. Parallelism is optional, not a target.

When TDD is enabled for new behavior, decide during planning whether RED and GREEN should be phases within one task or separate tasks. Consider scope, ownership, dependencies, and whether independent acceptance or a handoff adds value. Choose the structure that best supports execution and review. The task structure records the decision; include rationale only when useful. In either structure, plan for the intended behavioral failure before implementation, preserved accepted assertions and passing GREEN verification before completing work that includes implementation.

Distinguish settled contracts, decisions the worker may make locally, and unresolved decisions affecting shared behavior or dependent work. Resolve shared decisions before the affected implementation starts, or make bounded investigation/design work a prerequisite. Local implementation choices need not be settled in advance; ask the user only when the decision requires their input or changes authorized scope.

Where reasonable implementations could behave differently, acceptance criteria specify the intended observable result with a concrete example or invariant. Include boundary and failure behavior when it materially clarifies acceptance; avoid exhaustive case lists. Separate required behavior from suggested implementation. Keep durable scope, acceptance and shared decisions in task records or canonical contracts; worker assignments add current implementation state and immediate ownership without becoming another source of truth.

Read [execution.md](execution.md) when creating or materially revising the project protocol. Adapt the short working protocol in `../assets/project.template.md` to preserve scope, ownership, verification, TDD, logging and commit boundaries; keep detailed project-specific procedures in named project references. Reuse the existing protocol for additional work.

## Review requirements and complexity

Before finalizing, compare consequential requirements and design choices with the intended outcome, concrete use cases and existing constraints. Check whether agent suggestions or assumptions became commitments without explaining their cost or alternatives. User acceptance establishes a choice; it does not by itself establish that the implications were understood. Review the changed scope and relevant shared effects rather than reopening settled decisions unrelated to the request.

For a suspected unnecessary commitment or layer, identify a materially simpler viable alternative, the work or operating burden it removes, and any behavior or constraint it would compromise. Security, recovery, compatibility and established contracts can justify complexity. A pattern, abstraction or agent-proposed requirement is not automatically excessive, and fewer files or tasks is not proof of a better design.

Distinguish simplifications that preserve the user's outcome from proposals that change an explicit commitment. Explain the latter's practical tradeoff and obtain the user's decision before changing that commitment; continue unaffected planning meanwhile. Do not silently discard choices or claim to know the user's unstated intent. Retain concise rationale for consequential complexity when it is justified; avoid mandatory scorecards or review reports for small plans.

Use a separate bounded reviewer when architectural or scope commitments warrant independent judgment, such as costly-to-reverse choices or interacting constraints. Give the reviewer the proposed plan, intended outcome, relevant existing constraints and recorded decision context. Ask for concrete alternatives and tradeoffs, not blanket rejection or automatic rewriting. The orchestrator assesses and resolves findings before finalizing; unavailable review does not block ordinary planning unless required by the user or project rules. Small, straightforward additions need no extra reviewer.

## Review and maintain the handoff

Check the entire plan for incompatible contracts, missing ownership, hidden setup dependencies, cycles and unverified assumptions. Include integration work early enough to expose architectural mistakes. Check that the chosen RED/GREEN structure preserves tests-first verification when TDD applies; no artificial RED for existing correct behavior, setup, docs or final acceptance.

When an existing Python 3.9+ interpreter is available and permitted, run the skill’s `scripts/validate_plan.py PLAN_DIRECTORY`. It checks the task IDs, task-file links, dependencies, statuses and cycles in the PROJECT/TASKS layout; it cannot establish architecture quality. If no suitable permitted interpreter is available, review these structures manually and disclose that automated validation was not run; do not report the validator as passing. If the user or project explicitly requires the automated check, report unavailable tooling as a blocker. Fix meaningful defects, not just formatting. Review representative task scopes manually in either case.

When requirements change, update affected contracts, tasks, examples, testing guidance and register together. Routine task completion updates only the task record and register; edit PROJECT when its scope, policies, preferences or file map change. Do not reset progress or generate replacement task numbering casually. Mark obsolete/removed work `cancelled` with a reason; cancelled prerequisites do not count as completed—rewire dependencies explicitly.

Deliver the project guide and task register links, important decisions, unresolved blockers and the boundary between planning and execution. Creating a plan does not mean starting its tasks. If asked to execute later, follow the recorded plan settings and task protocol rather than re-asking settled preferences.
