from multiprocessing import Process
from pathlib import Path
import os
import sys
from typing import Dict, Any

def _run_spider(spider_name: str = "product_spider") -> None:
    try:
        project_root = Path(__file__).resolve().parents[2]
        scrapy_root = project_root / "scrapy"
        # garante que estamos no diretório do scrapy project e no PYTHONPATH
        os.chdir(str(scrapy_root))
        sys.path.insert(0, str(scrapy_root))
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "scrapy_datahunt.settings")

        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings

        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(spider_name)
        process.start()  
    except Exception:
        import traceback
        traceback.print_exc()

def start_scraper(spider_name: str = "product_spider") -> Dict[str, Any]:
    """
    Inicia a execução da spider em um processo separado e retorna info básica.
    """
    proc = Process(target=_run_spider, args=(spider_name,), daemon=True)
    proc.start()
    return {"pid": proc.pid, "spider": spider_name, "started": proc.is_alive()}
