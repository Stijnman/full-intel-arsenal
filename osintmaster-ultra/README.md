# OSINTMaster Ultra — functional domain-intelligence MVP

This replaces **mocked scan completions** with real, source-attributed results for
public domains. It is deliberately narrower than the draft OSINTMaster v3 specification.

## Run

Using Python standard library only:

```bash
cd osintmaster-ultra
python engine.py example.com
python -m unittest discover -s tests -v
```

Optional local Gradio web UI (Docker required):

```bash
docker compose up --build
# open http://localhost:8501
```

The Docker interface binds to localhost and runs as a non-root user.

## Implemented

- Validates and normalizes domain names.
- Resolves DNS A/AAAA through the system resolver.
- Blocks private, loopback, reserved, or mixed public/private IP responses.
- Uses TLS verification and performs one bounded HTTPS `HEAD /` request.
- Reports HTTP status, security headers, certificate expiry and TLS version.
- Returns machine-readable JSON and explicit error/skipped states.
- Includes offline unit tests.

## Not implemented

- 200+ modules, identity resolution, username/email/breach discovery.
- Certificate transparency, historical DNS, WHOIS, social scraping.
- Live graph, persistent case storage, reports or autonomous background tasks.

## Important

This is passive reconnaissance of public technical infrastructure only.
It does not prove security vulnerabilities. Obtain authorization before conducting
active testing. No private account discovery or personal-data correlation.

## Future milestones

1. Add provenance-preserving storage and export.
2. Add optional public certificate-transparency and RDAP enrichment.
3. Add offline fixtures and CI coverage for TLS errors and rate limits.
4. Integrate with the existing Gradio concept without demo placeholders.
