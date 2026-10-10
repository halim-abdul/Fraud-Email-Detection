from email.utils import parseaddr
from urllib.parse import urlparse
import ipaddress
import re

def sender_domain(sender: str) -> str:
    addr = parseaddr(sender)[1]
    return addr.rsplit("@", 1)[-1].lower() if "@" in addr else ""

def url_indicators(body: str) -> list[str]:
    flags = []
    for url in re.findall(r"https?://[^\\s<>]+", body, flags=re.I):
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("xn--") or ".xn--" in host:
            flags.append("punycode_domain")
        try:
            ipaddress.ip_address(host)
            flags.append("ip_literal_url")
        except ValueError:
            pass
        if "@" in urlparse(url).netloc:
            flags.append("url_userinfo")
    return sorted(set(flags))
