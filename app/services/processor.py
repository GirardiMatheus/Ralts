from typing import Iterable, List, Dict, Any, Tuple
from collections import Counter
import re

def _get_price(item: Any) -> float:
    try:
        if isinstance(item, dict):
            val = item.get("price")
        else:
            val = getattr(item, "price", None)
        if val is None:
            return None
        if isinstance(val, (int, float)):
            return float(val)

        s = str(val).strip()
        for ch in ["R$", "$", "€", "£", " "]:
            s = s.replace(ch, "")

        if "." in s and "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s and "." not in s:
            s = s.replace(",", ".")
        s = re.sub(r"[^\d\.-]", "", s)

        if not s:
            return None

        return float(s)
    except Exception:
        return None

def average_price(products: Iterable[Any]) -> float:
    total = 0.0
    count = 0
    for p in products:
        price = _get_price(p)
        if price is not None:
            total += price
            count += 1
    return (total / count) if count > 0 else 0.0

def _as_tuples_with_price(products: Iterable[Any]) -> List[Tuple[Any, float]]:
    rows = []
    for p in products:
        price = _get_price(p)
        if price is not None:
            rows.append((p, price))
    return rows

class ItemProxy:
    def __init__(self, obj: Any):
        self._obj = obj

    def get(self, key, default=None):
        return getattr(self._obj, key, default)

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __repr__(self):
        return f"<ItemProxy {repr(self._obj)}>"

def most_expensive(products: Iterable[Any], n: int = 1) -> List[Any]:
    rows = _as_tuples_with_price(products)
    rows.sort(key=lambda x: x[1], reverse=True)
    selected = [item for item, _ in rows[:max(0, n)]]
    return [s if isinstance(s, dict) else ItemProxy(s) for s in selected]

def cheapest(products: Iterable[Any], n: int = 1) -> List[Any]:
    rows = _as_tuples_with_price(products)
    rows.sort(key=lambda x: x[1])
    selected = [item for item, _ in rows[:max(0, n)]]
    return [s if isinstance(s, dict) else ItemProxy(s) for s in selected]

def count_by_category(products: Iterable[Any], key: str = "source") -> Dict[str, int]:
    counter = Counter()
    for p in products:
        try:
            if isinstance(p, dict):
                k = p.get(key)
            else:
                k = getattr(p, key, None)
            if k is None:
                k = "unknown"
            counter[str(k)] += 1
        except Exception:
            counter["unknown"] += 1
    return dict(counter)
