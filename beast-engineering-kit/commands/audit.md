# Command: AUDIT (`/audit`)

**Syntax:**
- `AUDIT`
- `audit`
- `/audit`
- `AUDIT: <path/diff>` / `audit <path/diff>`

## Description
Activates the Security Audit and Code Cleanliness (Deslop) workflows over target files or the current git diff.

## Standards & Focus Areas
1. **Security Audit (`security-audit`):**
   - Injection Defense (SQL, NoSQL, Command, LDAP).
   - Authentication & Authorization (IDOR, session hygiene).
   - SSRF & Safe HTTP Fetching.
   - Hardcoded Secrets & Credentials.
   - LLM & Agent Prompt Injection Protection.
2. **Deslop Cleanup (`deslop`):**
   - Diff-scoped anti-slop pass over git diff.
   - Strips comment narration, syntax restatements, defensive paranoia.
   - Eliminates type-laundering (`as any`, `@ts-ignore`).

## Visual Banner
```text
[AUDIT MODE ACTIVATED]
Workflow: Security Hardening & Deslop Cleanup
Owning Skills: security-audit, deslop
Standards: OWASP/CWE compliance, zero leaked secrets, zero AI slop
```

## Deactivation
Type `NORMAL` or `/normal` to return to standard AGY workflow.
