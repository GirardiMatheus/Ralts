import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any

from app.db.base import Base
from app.db.models import Product

logger = logging.getLogger(__name__)

class ProductPipeline:
    """
    Pipeline que salva items diretamente no banco SQLite do projeto usando SQLAlchemy sync.
    Mapeia item['title'] -> Product.name e item['price'] -> Product.price.
    """

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = None

    @classmethod
    def from_crawler(cls, crawler):
        # calcula path do DB relativo ao root do repo
        base_dir = Path(__file__).resolve().parents[3]
        db_path = base_dir / "ralts.db"
        db_url = f"sqlite:///{db_path}"
        return cls(db_url=db_url)

    def open_spider(self, spider):
        # garante que as tabelas existam
        Base.metadata.create_all(bind=self.engine)
        self.session = self.SessionLocal()
        logger.info("ProductPipeline: DB connected (%s)", self.db_url)

    def close_spider(self, spider):
        if self.session:
            self.session.close()
        try:
            self.engine.dispose()
        except Exception:
            pass
        logger.info("ProductPipeline: DB connection closed")

    def process_item(self, item: Dict[str, Any], spider):
        # mapear campos do item para o modelo Product
        name = item.get("title") or item.get("name") or "unknown"
        price = item.get("price")
        if price is None:
            price_value = 0.0
        else:
            try:
                price_value = float(price)
            except Exception:
                # tenta extrair números se price vier como string formatada
                try:
                    cleaned = str(price).replace(".", "").replace(",", ".")
                    price_value = float(cleaned)
                except Exception:
                    price_value = 0.0

        product = Product(name=name, price=price_value)
        try:
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            
            item["db_id"] = product.id
        except Exception as exc:
            self.session.rollback()
            logger.exception("Failed to save product: %s", exc)
        return item