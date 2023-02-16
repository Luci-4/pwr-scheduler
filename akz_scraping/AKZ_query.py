from akz_scraping.AKZ_fields import AKZFields

class AKZQuery(AKZFields):
    def __init_subclass__(cls) -> None:
        if cls == AKZQuery:
            raise TypeError("Cannot instantiate AKZQuery. Use child classes e.g. AKZQueryOr")
        return super().__init_subclass__()
    