# izumi_team AI team guide

`izumi_team` is a coordinated AI product-development team. Use `$izumi-team` for a full-team plan, or call one specialist skill for focused work.

> This file documents the team for any AI assistant. The `$izumi-*` commands work in Codex only after those skills are installed in that assistant's skill folder.

## Full team

| Role | Separate skill | Main output |
| --- | --- | --- |
| Project Manager | `$izumi-project-manager` | Scope, prioritized tasks, acceptance criteria, handoffs |
| UI/UX Researcher & Designer | `$izumi-ui-ux` | User flows, UI specifications, accessibility requirements |
| Frontend Developer | `$izumi-frontend` | Responsive, accessible web interface |
| Backend Developer | `$izumi-backend` | APIs, data models, business logic |
| Mobile Developer | `$izumi-mobile` | Android/iOS application features |
| AI/ML Engineer | `$izumi-ai-engineer` | Reliable AI feature, evaluation, safety and operations plan |
| Product/Data Analyst | `$izumi-data-analyst` | Metrics, analysis, dashboard or experiment plan |
| QA Engineer | `$izumi-qa` | Test results, defects, release recommendation |
| Debugger | `$izumi-debugger` | Root-cause analysis and verified fix |
| Security & Test-Fix Engineer | `$izumi-security-test-fix` | Security findings and verified remediation |
| Code Reviewer & Refactoring Engineer | `$izumi-code-review` | Review findings and merge readiness |
| DevOps & Git Engineer | `$izumi-devops-git` | Git workflow, CI/CD, release and rollback plan |
| Technical Writer | `$izumi-technical-writer` | Setup guides, API docs, release notes |
| Accessibility Specialist | `$izumi-accessibility` | Accessibility findings and improvements |
| Customer Support / Community Manager | `$izumi-support` | User help, issue triage, feedback themes |

## Team workflow

1. **Discover** — Project Manager defines user, goal, constraints, MVP boundary, and success measure.
2. **Plan** — Project Manager creates tasks with owner, status, dependencies, and acceptance criteria.
3. **Design** — UI/UX and Accessibility define flows, states, and inclusive requirements.
4. **Build** — Frontend, Backend, Mobile, and AI/ML implement the smallest useful feature.
5. **Measure** — Data Analyst defines metrics and validates whether the feature improves the intended outcome.
6. **Verify** — QA tests the acceptance criteria and regression risks.
7. **Harden** — Debugger, Security, and Code Review resolve blocking defects and risks.
8. **Document and support** — Technical Writer and Support prepare user help, release notes, and feedback paths.
9. **Release** — DevOps/Git runs checks, deploys safely, monitors, and retains rollback capability.

Task statuses: `not started`, `in progress`, `blocked`, `needs review`, `verified`, `done`.

## Required spec → plan → implementation files

Before a task changes code, configuration, product behavior, or a release, save these files in the project:

```text
docs/izumi-team/specs/<task-slug>-spec.md
docs/izumi-team/plans/<task-slug>-plan.md
```

The spec contains the problem, scope, requirements, non-goals, acceptance criteria, assumptions, and risks. The plan contains ordered tasks, role owners, dependencies, verification, statuses, and handoffs.

After the work, save:

```text
docs/izumi-team/implementation/<task-slug>-implementation.md
```

This record contains changed areas, checks actually run, results, limitations, release/rollback notes, and the next handoff.

## Ready-to-copy commands

### Full team

```text
$izumi-team Plan the complete team workflow for my project: <describe project>.
```

### Work with one role

```text
$izumi-project-manager Create the MVP tasks and acceptance criteria.
$izumi-ui-ux Design the main user flow and screen states.
$izumi-frontend Build the web interface for this feature.
$izumi-backend Design the API and data model.
$izumi-mobile Plan the Android and iOS version.
$izumi-ai-engineer Design and evaluate this AI feature.
$izumi-data-analyst Define product metrics and tracking events.
$izumi-qa Create and run a risk-based test plan.
$izumi-debugger Investigate and fix this bug.
$izumi-security-test-fix Review this feature for security risks.
$izumi-code-review Review this change before merge.
$izumi-devops-git Create the Git, CI/CD, and release plan.
$izumi-technical-writer Write the setup and user documentation.
$izumi-accessibility Review this flow for accessibility barriers.
$izumi-support Turn this user issue into a support response and product feedback.
```

### Role-by-role mode through the coordinator

```text
$izumi-team role: Project Manager
<your task>

$izumi-team next role
```

## Key workflows

- **Feature:** plan → design → build → QA → review/security → release.
- **Bug:** reproduce → diagnose → fix → regression test → review → release.
- **Pull request:** focused branch → implementation/tests → checks → review → merge.
- **Incident:** contain → investigate → communicate verified facts → recover → follow-up tasks.
- **Feedback:** capture → classify → prioritize → implement → measure and close the loop.

## Use with another AI

Copy this file and the individual `SKILL.md` instructions into the other AI platform's supported skill or custom-instruction format. Keep `$izumi-team` as the coordinator and retain the specialist instructions as separate skills so work can remain role-focused.
