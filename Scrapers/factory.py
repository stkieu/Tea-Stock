from Dict.Registry import ScraperRegistry

def get_scraper(site):
    scraper = ScraperRegistry.get_reg(site)
    if not scraper:
       raise ValueError(f"No scraper found for: {site}")
    return scraper