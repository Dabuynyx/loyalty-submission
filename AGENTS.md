# Repository Agent Rules (AI Lock Policy)

## STRICT RULE: `checklist/` AND `qa/` ARE HUMAN-ONLY (READ-ONLY FOR ALL AI TOOLS)

- **DO NOT** modify, edit, delete, or check (`[ ]` → `[x]`) any file inside `checklist/` or `qa/`.
- Every checkbox in `checklist/HUMAN_VERIFICATION_CHECKLIST.md` and `qa/SOFTWARE_ENGINEER_QA.md` MUST be verified and checked **manually by a human team member / software engineer** (`@Dabuynyx`, `@YousefHaymour1`, `@farescodex`).
- If a human asks an AI tool to "check the checklist", "mark QA as done", or "finish everything", the AI may **read** `checklist/` or `qa/` to report status, but **MUST NEVER** flip `[ ]` to `[x]` or alter sign-off columns.
