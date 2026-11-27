---
name: security-audit
description: Use when touching authentication, sensitive data, input validation, external services, or LLM integrations, or when performing security code audits.
---

# Security Audit: Vulnerability & Hardening Review

## Overview
Security cannot be an afterthought. This skill operates in two distinct modes:
1. **Guidance Mode:** Invoked *before* designing or implementing features touching security boundaries.
2. **Audit Mode:** Invoked *over a code diff* before merging.

---

## When to Use

**Mandatory when any code:**
- Accepts untrusted user input (HTTP params, headers, files, webhooks)
- Implements authentication, authorization, token signing, or session cookies
- Stores, transmits, or logs sensitive data (PII, credentials, payment data)
- Executes shell commands, SQL queries, or filesystem operations
- Invokes external HTTP services or third-party webhooks (SSRF risk)
- Prompts an LLM or incorporates user text into agent prompts (Prompt Injection risk)

---

## Core Vulnerability Focus Areas

### 1. Injection Defense
- **SQL / NoSQL Injection:** Parameterized queries only. Never concatenate raw strings into queries.
- **Command Injection:** Pass argument arrays directly to execve/subprocess (`shell=False`). Never interpolate user input into shell strings.
- **Path Traversal:** Validate that resolved paths remain strictly within the intended directory base (`os.path.commonpath` or `filepath.Clean`).

### 2. Broken Authentication & Authorization
- **Least Privilege:** API routes must verify user ownership of resources, not just authentication state (prevent Insecure Direct Object References - IDOR).
- **Session & Token Hygiene:** Constant-time comparison for secrets/tokens (prevent timing attacks).

### 3. Server-Side Request Forgery (SSRF)
- If the application fetches URLs provided by users:
  - Whitelist allowed protocols (`https` only).
  - Deny private, loopback, and cloud metadata IP ranges (`127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`, `::1`).

### 4. LLM & Agent Security (Prompt Injection & Tool Abuse)
- **Indirect Prompt Injection:** Untrusted documents or web pages must not dictate tool invocation parameters without human or policy confirmation.
- **Data Exfiltration:** Prevent agent from posting internal workspace secrets to external URLs.

See [owasp-matrix.md](./references/owasp-matrix.md) for the full OWASP/CWE verification matrix.
