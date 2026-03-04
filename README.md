# corp_os_meta

Shared metadata schema and taxonomy for the corp-by-os agent ecosystem. This package defines the frontmatter contract that all tools (knowledge-extractor, project-extractor, etc.) must follow when producing Obsidian vault notes. It provides Pydantic models for validation, a canonical taxonomy with alias resolution, and a CLI for vault health management.

## Installation

```bash
pip install -e C:\Users\1028120\Documents\Scripts\corp-os-meta
```

## Usage in Tools

```python
from corp_os_meta import NoteFrontmatter, normalize_frontmatter, validate_frontmatter

# 1. Build frontmatter dict from your extraction
data = {"title": "DR Overview", "date": "2026-01-15", "type": "presentation", ...}

# 2. Normalize taxonomy terms (DR → Disaster Recovery, BY WMS → Blue Yonder WMS)
data, changes, unknown = normalize_frontmatter(data)

# 3. Validate against schema — routes to vault or _quarantine/
result, note, issues = validate_frontmatter(data)
```

## CLI

```bash
# Validate a single note or entire vault
corp-meta validate path/to/note.md
corp-meta validate path/to/vault/ --recursive --strict

# Normalize taxonomy terms in-place
corp-meta normalize path/to/note.md --in-place

# Report on vault health
corp-meta report path/to/vault/
```

## Adding Taxonomy Terms

Edit `corp_os_meta/taxonomy.yaml`:

```yaml
topics:
  - name: "New Topic"
    aliases: ["alias1", "alias2"]
```

Rules:
- **Add** new terms freely
- **Never rename** without keeping the old name as an alias
- Products and topics each have their own section
- Aliases are case-insensitive

## Architecture

```
corp-os-meta (this package)
    ↑ imported by
corp-knowledge-extractor    — video/presentation extraction
corp-project-extractor      — file system scanning
corp-meeting-extractor      — meeting notes (future)
```

This is the FOUNDATION. All tools import `NoteFrontmatter` to ensure consistent, validated frontmatter across the entire Obsidian vault.
