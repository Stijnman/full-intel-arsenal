---
name: full-intel-arsenal
description: >
  Defensive competitive intelligence and open-source research skill. Combines
  public GitHub competitive analysis, OSINT hygiene, YouTube channel metrics
  review, and vulnerability-awareness research from public sources. Use when
  the user asks for competitor research, public repo scouting, channel stats,
  or defensive CVE awareness. Read-only; no exploit development.
version: 1.1.0
author: Stijnman
license: MIT
---

# Full Intel Arsenal (Defensive)

Unified agent skill for **public-source** competitive and security awareness research.

## When to use

- Competitive GitHub analysis (stars, activity, README quality, license)
- OSINT on **public** profiles and pages the user is allowed to review
- YouTube channel tooling (public metrics, upload cadence summaries)
- Vulnerability **awareness** from NVD/GHSA/public advisories (not 0-day weaponization)

## Workflow

1. Clarify target scope and legal/ethical boundary (public data only).
2. Gather sources in parallel: GitHub API/`gh`, web docs, advisory feeds.
3. Normalize findings into a structured report (markdown table + risks).
4. Separate **facts** from **hypotheses**; cite URLs.
5. Recommend defensive actions (patch, monitor, config harden) — never exploits.

## Modules

### A. Competitive GitHub analysis

- Repo metadata, languages, recent commits, open issues pulse
- README vs reality drift
- License and supply-chain surface (deps high-level only)

### B. OSINT (public)

- Public about pages, blogs, docs, status pages
- No credential stuffing, no private data access, no doxxing

### C. YouTube channel tools

- Public subscriber/video counts when available
- Upload frequency and topic clustering from titles

### D. Vulnerability intelligence (defensive)

- Map stack → known CVEs via public databases
- Prioritize by exposure and exploit **publication** status
- Output patch/upgrade guidance only

## Prohibited

- Writing exploit PoCs, malware, or attack playbooks
- Accessing private systems without authorization
- Harvesting personal data for harassment or spam

## Output format

```markdown
# Intel report: <target>
## Scope
## Key findings
## Competitive signals
## Security awareness
## Recommended next actions
## Sources
```

## Related skills

- `github-repo-scout`, `defensive-mcp-audit`, `competitor_researcher`, `skill-researcher`
