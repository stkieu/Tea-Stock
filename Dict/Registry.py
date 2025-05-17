class ScraperRegistry:
    registry = {}

    @classmethod
    def register(cls, name): #decorate to add each type of scraper to the register
        def dec(scraper):
            cls.registry[name] = scraper
            return scraper
        return dec
    
    @classmethod
    def get_reg(cls, name):
        return cls.registry.get(name)
        
