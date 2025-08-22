from cachetools import TTLCache
import httpx, pandas as pd

URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

_cache = TTLCache(maxsize=1, ttl=3600)  # 1 hour

def get_sp500_symbols() -> set[str]:
    #add retry
    if "symbols" in _cache:
        return _cache["symbols"]

    resp = httpx.get(URL, timeout=20)
    resp.raise_for_status()
    df = pd.read_html(resp.text)[0]
    symbols = set(df["Symbol"].str.upper())

    _cache["symbols"] = symbols
    return symbols
