from domain.models.dividend import Dividend
from domain.models.payment import Payment, PaymentFactory
from domain.services.countriesService import CountriesService
from domain.services.exchangeRateService import ExchangeRateService


class DividendsExchangeCalculator:
    _dividends: list[Dividend]
    _doFetchExchangeRate: bool

    def __init__(self, tax_percentage: int, do_fetch_exchange_rate: bool) -> None:
        Payment.taxPercentage = tax_percentage
        self._doFetchExchangeRate = do_fetch_exchange_rate

    def main(self, dividends: list[Dividend]) -> list[Dividend]:
        self._dividends = dividends

        self.__updateDividendsCountries()

        if self._doFetchExchangeRate:
            self.__updateDividendsExchangeRate()

        return self._dividends

    def __updateDividendsCountries(self) -> None:
        countriesService = CountriesService()

        for dividend in self._dividends:
            country = countriesService.fetchByCode(dividend.country)

            if country is not None:
                dividend.country = country

    def __updateDividendsExchangeRate(self) -> None:
        exchangeRateService = ExchangeRateService()
        currency = "USD"

        for dividend in self._dividends:
            exchangeRate = exchangeRateService.fetchAverageExchangeRate(
                currency, dividend.prevWorkingDateBeforePaid
            )

            paymentInUSD = dividend.getPaymentByCurrency(currency)

            if paymentInUSD is None:
                continue

            paymentInPLN = PaymentFactory.create("PLN", paymentInUSD.gross, paymentInUSD.withhold, exchangeRate)
            dividend.payments.append(paymentInPLN)
