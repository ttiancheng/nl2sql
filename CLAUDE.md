# NL2SQL Project — ESB2 Database Schema Knowledge Base

106 tables | 1631 fields | 102 logical FKs | 8 business domains

## Skill

`.claude/skills/nl2sql/SKILL.md` — auto-invoked when users ask Chinese business data questions (查/统计/看/找).

## How It Works

1. `esb2_table_scope_wiki.md` — table discovery map with Chinese descriptions and JOIN paths
2. `schemas/<table>.schema.json` — per-table field definitions with types, comments, and FK arrays
3. `execute_sql.py` — executes generated SQL against MySQL and returns JSON results
4. Progressive disclosure: find tables first → load schemas → generate SQL → execute & respond

## Quick Reference

- Table discovery: `.claude/skills/nl2sql/esb2_table_scope_wiki.md`
- Schema detail: `.claude/skills/nl2sql/schemas/<table>.schema.json`
