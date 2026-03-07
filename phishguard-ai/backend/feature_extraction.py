from __future__ import annotations

import ipaddress
import re
from typing import Iterable
from urllib.parse import urlparse

import numpy as np
import pandas as pd

IPV4_PATTERN = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def _ensure_scheme(url: str) -> str:
    if not isinstance(url, str):
        return ""
    cleaned = url.strip()
    if not cleaned:
        return ""
    if "://" not in cleaned:
        cleaned = f"http://{cleaned}"
    return cleaned


def _has_ip_in_domain(netloc: str) -> int:
    domain = netloc.split(":")[0]
    if not domain:
        return 0

    if IPV4_PATTERN.match(domain):
        try:
            ipaddress.ip_address(domain)
            return 1
        except ValueError:
            return 0

    if domain.startswith("[") and domain.endswith("]"):
        domain = domain[1:-1]
    try:
        ipaddress.ip_address(domain)
        return 1
    except ValueError:
        return 0


def extract_url_features(url: str) -> dict[str, int]:
    prepared = _ensure_scheme(url)
    parsed = urlparse(prepared)
    raw_url = prepared if prepared else ""

    return {
        "url_length": len(raw_url),
        "num_dots": raw_url.count("."),
        "num_hyphens": raw_url.count("-"),
        "num_digits": sum(ch.isdigit() for ch in raw_url),
        "num_slashes": raw_url.count("/"),
        "has_at_symbol": int("@" in raw_url),
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_ip_in_domain": _has_ip_in_domain(parsed.netloc),
    }


def extract_features_dataframe(urls: Iterable[str]) -> pd.DataFrame:
    series = pd.Series(list(urls), dtype="string").fillna("")
    prepared = series.str.strip()

    no_scheme_mask = ~prepared.str.contains(r"://", regex=True)
    prepared = prepared.mask(no_scheme_mask, "http://" + prepared)

    parsed = prepared.map(urlparse)
    netloc = parsed.map(lambda p: p.netloc)

    features = pd.DataFrame(
        {
            "url_length": prepared.str.len().astype(np.int32),
            "num_dots": prepared.str.count(r"\.").astype(np.int16),
            "num_hyphens": prepared.str.count(r"-").astype(np.int16),
            "num_digits": prepared.str.count(r"\d").astype(np.int16),
            "num_slashes": prepared.str.count(r"/").astype(np.int16),
            "has_at_symbol": prepared.str.contains("@", regex=False).astype(np.int8),
            "uses_https": parsed.map(lambda p: p.scheme.lower() == "https").astype(np.int8),
            "has_ip_in_domain": netloc.map(_has_ip_in_domain).astype(np.int8),
        }
    )
    return features