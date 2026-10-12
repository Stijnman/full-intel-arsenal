"""Offline unit tests; no external network access required."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine import normalize_domain, parse_http_headers, resolve_public_addresses, scan_domain


def record(ip):
    return (2, 1, 6, "", (ip, 443))


class DomainTests(unittest.TestCase):
    def test_domain_normalization(self):
        self.assertEqual(normalize_domain(" EXAMPLE.COM. "), "example.com")
        self.assertEqual(normalize_domain("sub.example.com"), "sub.example.com")

    def test_invalid_domain_inputs(self):
        for name in ("", "localhost", "https://example.com", "example.com/path",
                     "127.0.0.1", "bad_label.example.com", "example..com"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                normalize_domain(name)

    @patch("engine.socket.getaddrinfo", return_value=[record("8.8.8.8")])
    def test_public_dns_allowed(self, _mock):
        self.assertEqual(resolve_public_addresses("example.com"), ["8.8.8.8"])

    @patch("engine.socket.getaddrinfo",
           return_value=[record("8.8.8.8"), record("127.0.0.1")])
    def test_mixed_private_dns_blocked(self, _mock):
        with self.assertRaisesRegex(ValueError, "non-public"):
            resolve_public_addresses("example.com")

    def test_http_parser(self):
        status, headers = parse_http_headers(
            b"HTTP/1.1 301 Moved Permanently\r\n"
            b"Location: https://www.example.com/\r\n"
            b"Strict-Transport-Security: max-age=100\r\n\r\n"
        )
        self.assertEqual(status, 301)
        self.assertEqual(headers["strict-transport-security"], "max-age=100")
        self.assertEqual(headers["location"], "https://www.example.com/")

    @patch("engine.socket.getaddrinfo",
           return_value=[record("192.168.1.1")])
    def test_scan_skips_https_for_private_ip(self, _mock):
        result = scan_domain("example.com")
        self.assertEqual(result["modules"]["dns"]["status"], "error")
        self.assertEqual(result["modules"]["https"]["status"], "skipped")


if __name__ == "__main__":
    unittest.main()
