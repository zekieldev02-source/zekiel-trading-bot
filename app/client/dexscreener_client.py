"""DexScreener client — token price and market cap lookup (no API key required)."""

import logging
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

import httpx

_logger = logging.getLogger(__name__)

_BASE_URL = "https://api.dexscreener.com"
_TIMEOUT = 5.0
_MAX_PER_BATCH = 30


@dataclass(frozen=True)
class TokenMarketData:
    price: Decimal | None
    market_cap: Decimal | None


async def get_token_price(token_address: str) -> Decimal | None:
    """Returns the current native (SOL) price of a token, or None on failure."""
    result = await get_tokens_market_data([token_address])
    data = result.get(token_address)
    return data.price if data else None


async def get_tokens_market_data(
    token_addresses: list[str],
) -> dict[str, TokenMarketData]:
    """Batch-fetches price and market cap for up to 30 token addresses.

    Returns a dict keyed by token_address. Tokens not found are absent.
    """
    if not token_addresses:
        return {}

    unique = list(dict.fromkeys(token_addresses))
    batches = [unique[i: i + _MAX_PER_BATCH] for i in range(0, len(unique), _MAX_PER_BATCH)]

    result: dict[str, TokenMarketData] = {}
    async with httpx.AsyncClient(base_url=_BASE_URL, timeout=_TIMEOUT) as client:
        for batch in batches:
            batch_result = await _fetch_batch(client, batch)
            result.update(batch_result)

    return result


async def _fetch_batch(
    client: httpx.AsyncClient,
    addresses: list[str],
) -> dict[str, TokenMarketData]:
    result: dict[str, TokenMarketData] = {}
    try:
        resp = await client.get(f"/latest/dex/tokens/{','.join(addresses)}")
        resp.raise_for_status()
        pairs: list[dict] = resp.json().get("pairs") or []
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as exc:
        _logger.warning("DexScreener batch failed: %s", exc)
        return result

    addr_lower_map = {a.lower(): a for a in addresses}

    pairs_by_token: dict[str, list[dict]] = {}
    for pair in pairs:
        if pair.get("chainId") != "solana":
            continue
        raw_addr: str = (pair.get("baseToken") or {}).get("address", "").lower()
        original = addr_lower_map.get(raw_addr)
        if original:
            pairs_by_token.setdefault(original, []).append(pair)

    for token_address, token_pairs in pairs_by_token.items():
        best = max(
            token_pairs,
            key=lambda p: float((p.get("liquidity") or {}).get("usd") or 0),
        )

        price: Decimal | None = None
        price_str = best.get("priceNative")
        if price_str:
            try:
                price = Decimal(str(price_str))
            except InvalidOperation:
                pass

        market_cap: Decimal | None = None
        mc_raw = best.get("marketCap") or best.get("fdv")
        if mc_raw is not None:
            try:
                market_cap = Decimal(str(mc_raw))
            except InvalidOperation:
                pass

        if price is not None or market_cap is not None:
            result[token_address] = TokenMarketData(price=price, market_cap=market_cap)

    return result
