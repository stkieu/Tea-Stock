class ScraperRegistry:
    registry = {}
    hybrid_registry = {}

    @classmethod
    def register(cls, name): #decorate to add each type of scraper to the register
        def dec(scraper):
            cls.registry[name] = scraper
            return scraper
        return dec
    @classmethod
    def hybrid_register(cls, name):
        def dec(scraper):
            cls.hybrid_registry[name] = scraper
            return scraper
        return dec
    @classmethod
    def get_reg(cls, name):
        return cls.registry.get(name)
    @classmethod
    def get_hybrid_reg(cls,name):
        return cls.hybrid_registry.get(name)
        
