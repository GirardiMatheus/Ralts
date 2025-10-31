from app.services.processor import average_price, most_expensive, cheapest, count_by_category

class Dummy:
    def __init__(self, name, price, source=None):
        self.name = name
        self.price = price
        self.source = source

def test_average_price_and_extremes():
    items = [
        {"title": "A", "price": "1.000,50", "source": "s1"},
        {"title": "B", "price": "200.00", "source": "s1"},
        {"title": "C", "price": 150, "source": "s2"},
        Dummy("D", "2.500,00", "s2"),
        {"title": "E", "price": None, "source": "s3"},
    ]
    avg = average_price(items)
    assert abs(avg - 962.625) < 1e-6

    top2 = most_expensive(items, n=2)
    top_names = [getattr(p, "name", p.get("title")) for p in top2]
    assert "D" in top_names 

    cheap1 = cheapest(items, n=1)
    cheap_name = getattr(cheap1[0], "name", cheap1[0].get("title"))
    assert cheap_name == "C"

def test_count_by_category():
    items = [
        {"title": "A", "price": 10, "source": "s1"},
        {"title": "B", "price": 20, "source": "s1"},
        {"title": "C", "price": 5, "source": "s2"},
        {"title": "D", "price": None, "source": None},
    ]
    counts = count_by_category(items, key="source")
    assert counts == {"s1": 2, "s2": 1, "unknown": 1}
