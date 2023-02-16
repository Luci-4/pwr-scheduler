from akz_scraping.AKZ_fields import AKZFields
from akz_scraping.AKZ_query import AKZQuery
from dataclasses import dataclass

@dataclass
class AKZQueryAnd(AKZQuery):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def matches(self, found_fields: AKZFields):
        result = True
        for searched, found in zip(self.values, found_fields.values):
            test = searched.lower() in found.lower()
            result = result and test
        return result