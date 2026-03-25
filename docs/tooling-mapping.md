# Tooling Mapping

## Objective

This document maps the repository artifacts to common enterprise QA tools and workflows.

## TestRail Mapping

- `docs/testrail-test-cases.csv` represents structured test case inventory
- `docs/testrail-test-runs.csv` represents execution reporting
- `docs/test-cases.md` provides narrative detail that can back formal test case authoring

## Jira / Azure DevOps Mapping

- `docs/traceability-matrix.md` maps requirements and risks to coverage
- `docs/defect-report-example.md` reflects the expected defect content
- `docs/execution-summary-example.md` reflects release-quality reporting

## Confluence Mapping

- `docs/test-plan.md`
- `docs/test-strategy.md`
- `docs/agile-qa-delivery-model.md`
- `docs/test-estimation.md`
- `docs/design-review-checklist.md`

These documents can be migrated directly into a team wiki or documentation portal.

## Repository Value

The repository is intentionally tool-agnostic at implementation level, but the artifact structure aligns with common workflows used in:

- TestRail
- Jira
- Azure DevOps
- Confluence
- Bitbucket or GitHub-based CI review flows
