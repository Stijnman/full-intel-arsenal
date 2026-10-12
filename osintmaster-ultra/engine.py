"""Passive, public-domain OSINT collector. No scraping of people or private accounts."""
from __future__ import annotations

import ipaddress
import json
import re
import socket
import ssl
import sys
from datetime import datetime, timezone

MAX_HEADER_BYTES = 16384
SECURITY_HEADERS = (
    "strict-transport-security",
    "content-security-policy",
    "x-content-type-options",
    "referrer-policy",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_domain(value: str) -> str:
    """Accept a domain name, not a URL, IP address or path."""
    name = value.strip().rstrip(".")
    if not name or "://" in name or any(c in name for c in "/\\?#@:"):
        raise ValueError("Enter a domain only, such as example.com")
    try:
        name = name.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("Invalid domain encoding") from exc
    if len(name) > 253 or "." not in name:
        raise ValueError("A fully qualified domain name is required")
    try:
        ipaddress.ip_address(name)
    except ValueError:
        pass
    else:
        raise ValueError("IP address inputs are not supported")
    for label in name.split("."):
        if not (1 <= len(label) <= 63) or not re.fullmatch(
            r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", label
        ):
            raise ValueError("Invalid domain label")
    if name.split(".")[-1].isdigit():
        raise ValueError("Invalid top-level domain")
    return name


def resolve_public_addresses(domain: str) -> list[str]:
    """Resolve addresses; fail closed if *any* resolved IP is not public."""
    records = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
    addresses = sorted({record[4][0] for record in records})
    if not addresses:
        raise ValueError("No DNS addresses returned")
    if any(not ipaddress.ip_address(addr).is_global for addr in addresses):
        raise ValueError("DNS resolves to a non-public address; scan blocked")
    return addresses


def parse_http_headers(raw: bytes) -> tuple[int | None, dict[str, str]]:
    """Parse a bounded HTTP response header block."""
    text = raw.split(b"\r\n\r\n", 1)[0].decode("iso-8859-1", errors="replace")
    lines = text.split("\r\n")
    match = re.match(r"^HTTP/\d(?:\.\d)?\s+(\d{3})", lines[0])
    status = int(match.group(1)) if match else None
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip():
                headers[key.strip().lower()] = value.strip()
    return status, headers


def probe_https(domain: str, addresses: list[str], timeout: float = 5.0) -> dict:
    """Inspect TLS and HTTPS HEAD / without following redirects or fetching bodies."""
    timeout = min(max(float(timeout), 1.0), 10.0)
    last_error = "No reachable public address"
    for address in addresses[:3]:
        try:
            with socket.create_connection((address, 443), timeout=timeout) as sock:
                with ssl.create_default_context().wrap_socket(
                    sock, server_hostname=domain
                ) as tls:
                    tls.settimeout(timeout)
                    certificate = tls.getpeercert()
                    tls.sendall(
                        (f"HEAD / HTTP/1.1\r\nHost: {domain}\r\n"
                         "User-Agent: OSINTMaster-Ultra/0.1\r\n"
                         "Connection: close\r\n\r\n").encode("ascii")
                    )
                    data = b""
                    while b"\r\n\r\n" not in data and len(data) < MAX_HEADER_BYTES:
                        part = tls.recv(min(4096, MAX_HEADER_BYTES - len(data)))
                        if not part:
                            break
                        data += part
                    status, headers = parse_http_headers(data)
                    if status is None:
                        raise ValueError("Invalid HTTPS header response")
                    return {
                        "status": "ok",
                        "source": f"https://{domain}/",
                        "ip_used": address,
                        "http_status": status,
                        "tls_version": tls.version(),
                        "certificate_expires": certificate.get("notAfter"),
                        "certificate_subject": certificate.get("subject"),
                        "security_headers": {
                            key: headers.get(key) for key in SECURITY_HEADERS
                        },
                        "redirect_location": headers.get("location"),
                        "checked_at": utc_now(),
                    }
        except (OSError, ssl.SSLError, ValueError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
    return {
        "status": "error",
        "source": f"https://{domain}/",
        "error": last_error,
        "checked_at": utc_now(),
    }


def scan_domain(value: str, timeout: float = 5.0) -> dict:
    """Public-domain DNS + HTTPS inspection with transparent provenance."""
    domain = normalize_domain(value)
    result = {
        "target": domain,
        "type": "public_domain",
        "checked_at": utc_now(),
        "modules": {},
        "disclaimer": "Passive snapshot; missing headers alone do not prove a vulnerability.",
    }
    try:
        addresses = resolve_public_addresses(domain)
        result["modules"]["dns"] = {
            "status": "ok", "source": f"DNS for {domain}",
            "addresses": addresses, "checked_at": utc_now(),
        }
    except (OSError, ValueError) as exc:
        result["modules"]["dns"] = {
            "status": "error", "source": f"DNS for {domain}",
            "error": f"{type(exc).__name__}: {exc}", "checked_at": utc_now(),
        }
        result["modules"]["https"] = {
            "status": "skipped", "reason": "DNS did not pass the public-IP gate"
        }
        return result
    result["modules"]["https"] = probe_https(domain, addresses, timeout)
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python engine.py example.com", file=sys.stderr)
        sys.exit(2)
    try:
        print(json.dumps(scan_domain(sys.argv[1]), indent=2))
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        sys.exit(2)
