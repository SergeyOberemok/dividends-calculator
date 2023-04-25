
from ..models.country import Country


class CountriesService:
    def fetch(self) -> list[Country]:
        return [
            Country("US", "United States", True),
            Country("GB", "United Kingdom", True),
            Country("CA", "Canada", True),
            Country("GG", "Guernsey", True),
            Country("IE", "Ireland", True),
            Country("CH", "Switzerland", True),
        ]

    def fetchByCode(self, code: str) -> Country:
        return next((country for country in self.fetch() if country == code), None)
