import httpx
import pandas as pd
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential

URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


class WikipediaClient:
    #TODO: inject in dependencies and validation on the symbols from the endpoint not the schema
    _cache = TTLCache(maxsize=1, ttl=3600)  # 1 hour cache

    @classmethod
    def get_sp500_symbols(cls) -> set[str]:
        """Return cached symbols or fetch if expired."""
        if "symbols" in cls._cache:
            return cls._cache["symbols"]
        symbols = cls._fetch_symbols()
        cls._cache["symbols"] = symbols
        return symbols

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _fetch_symbols() -> set[str]:
        """Fetch symbols from Wikipedia with retry."""
        resp = httpx.get(URL, timeout=20, headers={"User-Agent": "PredictionService/1.0"})
        resp.raise_for_status()
        df = pd.read_html(resp.text)[0]
        return set(df["Symbol"].astype(str).str.upper().str.strip())
