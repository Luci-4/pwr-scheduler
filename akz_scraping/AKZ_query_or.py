from akz_scraping.AKZ_query import AKZQuery
from akz_scraping.AKZ_fields import AKZFields

from dataclasses import dataclass

@dataclass
class AKZQueryOr(AKZQuery):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def matches(self, found_fields: AKZFields):
        result = False
        for searched, found in zip(self.values, found_fields.values):
            result = result or (searched.lower() in found.lower())
        return result
