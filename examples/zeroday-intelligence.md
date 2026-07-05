# Example: 0-Day Intelligence

**Input:**
```
What are the current actively exploited critical 0-days affecting web infrastructure, and how should I mitigate them right now if no patch is available?
```

**What the skill does:**
- Pulls from CISA KEV, NVD, GitHub Advisories, and real-time sources
- Focuses on actively exploited vulnerabilities
- Provides immediate compensating controls + WAF rules when relevant
- Follows responsible disclosure principles

**Expected Output Style:**
- Executive Summary of active threats
- Table of relevant CVEs with severity, exploitation status, and patch availability
- Immediate mitigation strategies (no-patch)
- WAF / hardening examples where useful
- Recommended ongoing monitoring approach

**Why this is valuable:**
Turns scattered vulnerability data into actionable defensive guidance fast.