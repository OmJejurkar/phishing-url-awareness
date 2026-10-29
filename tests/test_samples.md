# Test Results

Python version used: 3.12.10 | Operating system: Windows 11 | Date: 2026-10-28

| # | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| 1 | https://www.example.com/login | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP address + HTTP | Uses an IP address instead of a familiar domain. <br> Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol + HTTP | Contains an @ symbol; inspect carefully. <br> Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Notes
- I learned that static text inspection can rapidly detect deceptive URL techniques like `@` prefix redirection, bare IP addresses, and punycode homoglyphs without any network footprint.
- What surprised me most was that an absence of warning signs does NOT guarantee security (`https://secure-login.example.invalid` has zero warnings yet could easily be a deceptive spoof).
- In addition, handling malformed inputs like `http://[bad` via safe parsing prevents runtime exceptions and keeps the tool robust against irregular strings.
