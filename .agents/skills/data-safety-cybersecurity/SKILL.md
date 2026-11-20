---
name: data-safety-cybersecurity
description: Production web security and data protection. Defense-in-depth, OWASP Top 10 mitigation, SQL injection prevention, XSS/CSRF hardening, secret scanning, and encryption standards.
---

# Data Safety & Cybersecurity Skill

## 1. OWASP Top 10 Hardening
- **SQL Injection**: Never interpolate strings into SQL. Always use parameterized queries (`? ` or `:param`).
- **Cross-Site Scripting (XSS)**: Automatically escape all HTML outputs in templates; avoid `innerHTML` and `v-html`.
- **Cross-Site Request Forgery (CSRF)**: Issue cryptographically secure SameSite cookies (`SameSite=Lax` or `Strict`) with Anti-CSRF tokens.
- **Sensitive Data Exposure**: Hash all passwords with PBKDF2, bcrypt, or Argon2id. Never log raw passwords, tokens, or personal identifiers.

## 2. Automated Security Audits
- Run `npx guardvibe scan .` and `snyk code test` prior to code merges.
- Prevent credential leaks: ensure `.env*` files are included in `.gitignore`.
