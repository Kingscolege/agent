# OWASP & CWE Verification Matrix

| Vulnerability Category | Common Root Causes | Mandatory Verification Standard |
|---|---|---|
| **SQL Injection (CWE-89)** | String formatting into queries | Query uses positional or named bind parameters ($1, ?, :param). |
| **Command Injection (CWE-78)** | `subprocess.run(f"cmd {input}", shell=True)` | Arguments passed as array: `["cmd", input]`, `shell=False`. |
| **Path Traversal (CWE-22)** | Joining untrusted filenames directly | Resolve canonical path; verify `canonical.startswith(allowed_root)`. |
| **SSRF (CWE-918)** | Fetching unvalidated user-supplied URLs | Reject localhost, private subnets (RFC 1918), and link-local addresses. |
| **Hardcoded Secrets (CWE-798)** | API keys, JWT secrets in source code | Read from environment variables or Secret Manager; zero literals in code. |
| **XSS (CWE-79)** | Unescaped HTML rendering | Contextual HTML entity escaping or framework-managed templating. |
| **Insecure Deserialization (CWE-502)** | `pickle.loads()`, `yaml.load()` | Use safe parsers: `json.loads()`, `yaml.safe_load()`. |
| **Timing Attacks (CWE-208)** | `secret == user_token` | Use constant-time equality check (`hmac.compare_digest`). |
