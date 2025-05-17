from Dict.Registry import ScraperRegistry

def get_scraper(site):
    scraper = ScraperRegistry.get_reg(site)
    if not scraper:
        return ValueError(f"No scraper found")
    return scraper