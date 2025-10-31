from fastapi.testclient import TestClient
import app.main as main
import app.api.routes as routes

def test_healthcheck():
    client = TestClient(main.app)
    resp = client.get("/healthcheck")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_scrape_start_monkeypatched(monkeypatch):
    def fake_start_scraper(spider_name="product_spider"):
        return {"pid": 9999, "spider": spider_name, "started": True}

    monkeypatch.setattr(routes, "start_scraper", fake_start_scraper)
    client = TestClient(main.app)
    resp = client.post("/scrape/start")
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "started"
    assert data["pid"] == 9999
    assert data["spider"] == "product_spider"
