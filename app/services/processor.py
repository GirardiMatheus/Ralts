from typing import Iterable, List, Dict, Any, Tuple
from collections import Counter

def _get_price(item: Any) -> float:
    """
    Extrai o preço de um item (dict ou objeto). Retorna None se não for possível.
    """
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
        for ch in ["R$", "$", "€", "£"]:
            s = s.replace(ch, "")
        s = s.replace(".", "").replace(",", ".")
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

def most_expensive(products: Iterable[Any], n: int = 1) -> List[Any]:
    rows = _as_tuples_with_price(products)
    rows.sort(key=lambda x: x[1], reverse=True)
    return [item for item, _ in rows[:max(0, n)]]

def cheapest(products: Iterable[Any], n: int = 1) -> List[Any]:
    rows = _as_tuples_with_price(products)
    rows.sort(key=lambda x: x[1])
    return [item for item, _ in rows[:max(0, n)]]

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
