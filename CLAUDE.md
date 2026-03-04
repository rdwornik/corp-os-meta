# CLAUDE.md — corp_os_meta

## Workflow

- Read `tasks/todo.md` at session start for current priorities
- Log discoveries in `tasks/lessons.md`
- Run `pytest tests/ -v` after every change
- Keep code under 300 lines total (excluding tests and taxonomy)

## Engineering Principles

- Simple > clever. Minimal abstractions.
- Every function must have tests.
- No silent failures — log warnings, raise on errors.
- Taxonomy changes must be backward-compatible.

## Project-Specific: corp_os_meta

This package defines the metadata CONTRACT for all corp-by-os tools.
Changes here affect EVERY tool in the ecosystem.

### Rules
- taxonomy.yaml changes must be backward-compatible (add, never rename without alias)
- New required fields in NoteFrontmatter = schema_version bump
- New optional fields = no version bump needed
- <300 lines of code total (excluding tests and taxonomy)
- Every function must have tests
- This package has ZERO external dependencies beyond pydantic, pyyaml, click, rich

### Key Files
- `corp_os_meta/models.py` — Pydantic models (the contract)
- `corp_os_meta/normalize.py` — taxonomy loading + term normalization
- `corp_os_meta/validate.py` — validation + quarantine routing
- `corp_os_meta/taxonomy.yaml` — canonical terms + aliases
- `cli.py` — Click CLI for vault management

### Testing
```bash
pytest tests/ -v
python -c "from corp_os_meta import NoteFrontmatter; print('OK')"
```
