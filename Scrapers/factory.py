from Dict.Registry import ScraperRegistry

def get_scraper(site):
   scraper = ScraperRegistry.get_reg(site)
   if not scraper:
      raise ValueError(f"No scraper found for: {site}")
   return scraper
def get_hybrid_scraper(site):
   scraper = ScraperRegistry.get_hybrid_reg(site)
   if not scraper:
      raise ValueError(f"No hybrid scraper found for: {site}")
   return scraper