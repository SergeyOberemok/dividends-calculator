import pytest
from ...services.countriesService import CountriesService
from ...models.country import Country


@pytest.fixture
def countriesService() -> CountriesService:
    return CountriesService()


def test_fetchByCodeSuccess(countriesService: CountriesService) -> None:
    code = 'US'

    result = countriesService.fetchByCode(code)

    assert isinstance(result, Country)
    assert result == code


def test_fetchByCodeFail(countriesService: CountriesService) -> None:
    code = 'test'

    result = countriesService.fetchByCode(code)

    assert result is None
