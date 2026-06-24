---
name: nl2sql
description: >
  Chinese NL→MySQL for ESB2 CRM/ERP database (106 tables, 1631 fields, 102 FKs).
  Covers customers, suppliers, contacts, sales opportunities, pre-sale actions,
  contracts, approvals, invoicing, payments, bad debts, expenses, cost spaces,
  products, materials, BOMs, projects, after-sale, news, users, roles, logs.
  Use when user asks data questions like 查/统计/看/找/列出 or asks to write SQL.
user-invocable: true
---

# ESB2 NL2SQL Skill

This skill translates Chinese business questions into MySQL queries against the ESB2 CRM/ERP database using progressive disclosure: find tables first, then load schemas, then generate SQL, then execute and return results.

## Data Sources

| File | Purpose | When to Load |
|:-----|:--------|:-------------|
| `esb2_table_scope_wiki.md` | Table discovery map — 106 tables with Chinese descriptions, primary keys, outgoing/incoming logical FKs, organized by 8 business domains | Step 1 — always first |
| `schemas/<table>.schema.json` | Per-table field definitions — field names, types, nullable, defaults, Chinese comments, and `foreign_keys` array for JOIN conditions | Step 2 — only for identified candidate tables |
| `execute_sql.py` | Python helper — reads SQL from stdin, executes against MySQL via PyMySQL, returns JSON | Step 4 — always after generating SQL |

## Four-Step Workflow

### Step 1: Discover Tables

Read `esb2_table_scope_wiki.md` to identify which tables are relevant:

1. Scan the 8 domain sections for Chinese keywords from the user's question.
2. Identify the **fact table** (the main business event table) and any **dimension/lookup tables**.
3. Use the "本表逻辑外键" (outgoing FK) and "被哪些表引用" (incoming FK) sections to map JOIN paths.
4. Output a list of candidate tables before proceeding to Step 2.

### Step 2: Load Schemas

For each candidate table, read `schemas/<table>.schema.json`.

From each schema, extract:
- **Field names** — to write correct SELECT and JOIN columns
- **Chinese comments** (`comment`) — to write semantically correct WHERE filters
- **Data types** (`data_type`) — for type-aware SQL (e.g. `int(11)` for dates, `varchar` for text)
- **`foreign_keys` array** — each entry is `{"column": "...", "references": {"table": "...", "column": "..."}}` — this is the authoritative JOIN condition

### Step 3: Generate SQL

1. Write MySQL-compatible SQL using `zzvc_` table names directly.
2. Use the `foreign_keys` array from Step 2 as the authoritative JOIN source:
   - `foreign_key.column` is the FK column in **this** table
   - `foreign_key.references.table` and `foreign_key.references.column` identify the target
3. Use LEFT JOIN for optional dimension tables, INNER JOIN only when both sides always have records.
4. Add table aliases: `cl` for `zzvc_contract_list`, `u` for `zzvc_user`, `cc` for `zzvc_company_customer`.
5. Handle date fields stored as `int(11)` with `FROM_UNIXTIME()` for display, `UNIX_TIMESTAMP()` for filtering.
6. Proceed to Step 4 to execute the SQL and return results to the user.

### Step 4: Execute SQL and Respond

Execute the generated SQL against the ESB2 MySQL database and present results using these rules.

**4a. Execute the SQL**

Use the `execute_sql.py` helper with a **quoted heredoc** (`<<'EOSQL'` — the single quotes around the delimiter are critical to prevent shell expansion of Chinese characters and SQL special characters):

```bash
python3 /home/roger/projects/nl2sql/.claude/skills/nl2sql/execute_sql.py <<'EOSQL'
<generated SQL>
EOSQL
```

The script outputs a single JSON object on stdout with one of two shapes:

- **Success**: `{"success": true, "columns": [...], "rows": [...], "row_count": N, "truncated": bool, "elapsed_seconds": float}`
- **Error**: `{"success": false, "error": "...", "error_code": int, "elapsed_seconds": float}`

**4b. Format results based on content type**

| Result Type | Display Strategy |
|:------------|:-----------------|
| **0 rows** | "没有找到匹配的数据。" — suggest checking filter values, offer to show SQL. |
| **1–20 rows, general** | Full Markdown table (`|col|col|`) with header row, row count, and elapsed time. |
| **1 row, aggregate** (single COUNT/SUM/AVG/GROUP BY with 1 result) | Show the value directly and prominently. No table needed. |
| **21–200 rows** | Full Markdown table. Note: "共 N 行". |
| **200+ rows (truncated)** | The script caps at 200 rows (`truncated: true`). Show the table with note: "结果超过200行，仅显示前200行。如需完整数据请添加更精确的筛选条件。" |
| **Error (DB unreachable)** | Inform user MySQL at the detected host is unreachable. Offer to show SQL only. |
| **Error (SQL syntax)** | Show the error message. Check if field/table names are correct and retry with corrected SQL. |

**4c. Write a Chinese summary**

Always follow the table (or aggregate value) with a 1–2 sentence Chinese natural-language summary that restates the question, the key numbers, and any notable patterns.

**4d. SQL visibility**

- **By default**: show the SQL in a collapsible or separate ` ```sql ` block so the user can verify it, followed by results and summary.
- **If the user explicitly asked for "SQL only"**: show only the SQL, skip execution.
- **If the user asked for results only (no SQL)**: skip the SQL block, show only results and summary.

## Principles

- **Never hallucinate** table names, field names, or FK relationships. Always verify from the schemas.
- **Choose the most specific table**: `zzvc_contract_list` (new contract ledger) over `zzvc_contract` (old contract table) when the question is about contract details, payments, or invoicing.
- **If ambiguous**, state your assumptions and offer to refine the query.
- **If asked for SQL only**, skip the explanation.
- **Always execute automatically** after generating SQL, unless the user explicitly asked for "SQL only". The skill has direct database access via `execute_sql.py` and PyMySQL.

## Domain Quick Reference

| Domain | Key Tables | Common Keywords |
|:-------|:-----------|:----------------|
| 用户/权限 | `zzvc_user`, `zzvc_role`, `zzvc_category` | 用户, 角色, 权限, 菜单 |
| 客户/供应商 | `zzvc_company_customer`, `zzvc_company_customer_contract`, `zzvc_tax` | 客户, 供应商, 联系人, 开票 |
| 商机/销售 | `zzvc_business_chance`, `zzvc_business_before_sale`, `zzvc_business_chance_follow` | 商机, 销售机会, 跟进, 售前 |
| 合同/审批 | `zzvc_contract_list`, `zzvc_contract_review`, `zzvc_contract_sheet`, `zzvc_dd_open_bill` | 合同, 审批, 回款, 开票, 坏账 |
| 费用/成本 | `zzvc_expenses`, `zzvc_order`, `zzvc_meeting_room`, `zzvc_cost_detail_log` | 费用, 报销, 成本, 差旅 |
| 产品/物料 | `zzvc_materiel`, `zzvc_device_metrics`, `zzvc_device_basic_bom` | 产品, 物料, 设备, BOM |
| 项目/售后 | `zzvc_after_sale`, `zzvc_integration_projects`, `zzvc_project_daily` | 项目, 售后, 工程, 日报 |
| 新闻/日志 | `zzvc_news`, `zzvc_comment`, `zzvc_my_log`, `zzvc_notice` | 新闻, 评论, 日志, 通知 |
