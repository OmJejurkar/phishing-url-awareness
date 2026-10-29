"""
EWB Cybersecurity Mini Project: Phishing URL Awareness Checker
A defensive, educational command-line tool that inspects URL text
for visible phishing warning signs without making network requests.
"""

import re
from urllib.parse import urlparse

# Informational messages that are not security warnings
INFO_MESSAGES = (
    "No URL entered.",
    "Could not identify a hostname.",
    "This text is not a valid URL format.",
    "No listed warning signs found. This does NOT prove safety."
)

# Educational explanations for each warning indicator (Improvement D)
WARNING_EXPLANATIONS = {
    "Contains an @ symbol; inspect carefully.": 
        "Browsers ignore text before '@' for routing, which attackers use to mimic legitimate domains.",
    "Unusually long URL (over 100 characters).": 
        "Excessively long links can obscure the true destination or bury suspicious parameters.",
    "Uses an IP address instead of a familiar domain.": 
        "Legitimate brands typically use domain names; bare IP addresses bypass domain reputation checks.",
    "Contains many hostname segments/subdomains.": 
        "Excessive subdomain levels (5+) are frequently stacked to create a deceptive appearance of authority.",
    "Contains a punycode-style hostname.": 
        "Punycode ('xn--') allows non-ASCII characters that can visually spoof trusted brand names.",
    "Uses HTTP. HTTPS alone does not prove trust.": 
        "HTTP connections are unencrypted in transit. (Note: HTTPS alone does not guarantee authenticity)."
}


def inspect_url(raw_url: str) -> list[str]:
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    # Prepend scheme if missing so urlparse can extract the host correctly
    candidate = url if "://" in url else "http://" + url

    # Improvement C: Safe URL parsing to prevent crashes on malformed inputs (e.g. invalid IPv6 brackets)
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()

    if not host:
        return ["Could not identify a hostname."]

    # Check 1: @ symbol
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Check 2: Unusually long URL
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Check 3: IP address as hostname
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Check 4: Hostname segments (subdomains)
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Check 5: Punycode marker
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # Check 6: HTTP scheme check
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    # Default message when no clues are found
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def has_warnings(findings: list[str]) -> bool:
    """Check whether any finding in the list represents an actual warning sign."""
    if not findings:
        return False
    return not any(findings[0].startswith(msg) for msg in INFO_MESSAGES)


def main():
    """Interactive CLI runner with loop, quit command, and summary (Improvements A & B)."""
    print("=" * 50)
    print("       EWB Phishing URL Awareness Checker        ")
    print("=" * 50)
    print("Text checks only - this program does not open URLs.")

    while True:
        raw_url = input("\nEnter a sample URL (or type q to quit): ")
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")
        for item in findings:
            print("- " + item)
            # Display educational explanation if available
            if item in WARNING_EXPLANATIONS:
                print("  ↳ Why it matters: " + WARNING_EXPLANATIONS[item])

        if has_warnings(findings):
            print(f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found.")

        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
