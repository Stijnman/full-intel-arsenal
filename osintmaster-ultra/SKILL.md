---
name: osintmaster-ultra
description: Evidence-backed passive public-domain reconnaissance with DNS and HTTPS checks.
---

# OSINTMaster Ultra — operational MVP

## Scope
Only domains with publicly resolvable IP addresses. No personal-account discovery,
phone/email harvesting, breach scraping, credential testing, or private resources.

## Workflow
1. Receive a public domain name, without URL syntax.
2. Run `python engine.py example.com` from this directory.
3. Report DNS resolution and HTTPS HEAD response with source and timestamp.
4. Distinguish `ok`, `error` and `skipped` states; never convert errors into findings.
5. Provide findings and limitations; never invent data or classify header absence as proof of compromise.

## Optional interface
Run `docker compose up --build`, then visit http://localhost:8501.

## Safety and reliability
- Fails closed for non-global IPs and DNS responses mixing global/non-global IPs.
- Connects only to resolved public IPs; never follows HTTP redirects.
- Validates TLS certificates and uses bounded HTTP header reads.
- Does not enumerate people or associate identity across platforms.
- This directory is an operational *MVP*, not the 200-module v3 concept.
