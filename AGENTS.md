# AGENTS.md — okc (Open Knowledge CLI)

## Git Workflow
When making code changes ALWAYS follow this process:

1. Ensure current branch is committed if not do not continue until the user has committed and pushed the changes.

2. Create a new branch before editing:
   git checkout -b agent/<short-task-name>

3. Never commit directly to main or master.

4. Use clear commit messages:
   feat: ...
   fix: ...
   refactor: ...

## Mandatory Rules

These rules must always be followed:
- NEVER make changes unless the current branch is committed.
- ALWAYS create a git branch before editing code.
- NEVER modify protected branches.
- ALWAYS run tests before committing.
- ALWAYS check if the code is commited.
- NEVER archive changes before committing.