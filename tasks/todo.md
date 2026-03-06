# TODO — corp_os_meta

## Done
- [x] Initial package structure
- [x] Pydantic models (NoteFrontmatter, DocumentType, QualityLevel)
- [x] Taxonomy YAML with topics, products, document types
- [x] Normalization engine (alias resolution, dedup, caps)
- [x] Validation + quarantine routing
- [x] CLI (validate, normalize, report)
- [x] Tests for all modules

## Done (v1.1)
- [x] Smart preprocessing layer (parentheticals, plurals, ampersands, whitespace)
- [x] Two-pass matching: exact first, preprocessed fallback
- [x] Added "SaaS" alias to SaaS Architecture

## Backlog
- [ ] Integrate into corp-knowledge-extractor (replace local taxonomy)
- [ ] Integrate into corp-project-extractor
- [ ] Add more taxonomy terms as new content is processed
- [ ] Add `corp-meta taxonomy` CLI command to list/search terms
