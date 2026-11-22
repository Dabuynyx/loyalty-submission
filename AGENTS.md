# Repository Agent Rules (AI Lock Policy)

## STRICT RULE: `checklist/` IS HUMAN-ONLY (READ-ONLY FOR ALL AI TOOLS)

- **DO NOT** modify, edit, delete, or check (`[ ]` → `[x]`) any file inside `checklist/`.
- Every checkbox in `checklist/HUMAN_VERIFICATION_CHECKLIST.md` MUST be verified and checked **manually by a human team member** (`@Dabuynyx`, `@YousefHaymour1`, `@farescodex`).
- If a human asks an AI tool to "check the checklist" or "finish everything", the AI may **read** `checklist/` to report status, but **MUST NEVER** flip `[ ]` to `[x]` or alter sign-off columns.
