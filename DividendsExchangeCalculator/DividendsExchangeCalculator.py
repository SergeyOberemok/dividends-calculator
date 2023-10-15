
from domain.services.dividendsReader import IReader, DividendsCsvReader
from domain.services.dividendsWriter import (
    IWriter,
    DividendsConsoleWriter,
    DividentsSummaryConsoleWriter,
)
from domain.services.exchangeRateService import ExchangeRateService
from domain.services.countriesService import CountriesService
from domain.models.dividend import Dividend
from domain.models.payment import Payment, PaymentFactory


class DividendsExchangeCalculator:
    taxPercentage: int = 19

    _dividends: list[Dividend]
    _doesFetchExchangeRate: bool

    def __init__(self) -> None:
        taxPercentageAnswer = input(
            f"Enter tax percentage (default {self.taxPercentage}) "
        )
        self.taxPercentage = (
            self.taxPercentage
            if taxPercentageAnswer == ""
            else int(taxPercentageAnswer)
        )
        Payment.taxPercentage = self.taxPercentage

        self._doesFetchExchangeRate = (
            True if input("Fetch exchange rate [y/N] ") == "y" else False
        )

    def main(self) -> None:
        self.__fetchDividends()

        self.__updateDividendsCountries()

        if self._doesFetchExchangeRate == True:
            self.__updateDividendsExchangeRate()

        self.__outputDividends()

    def __fetchDividends(self) -> None:
        fileName = "sources\\2022.dividends.csv"
        parseDateFormat: str = "%Y%m%d"
        parseDelimiter: str = ","
        reader: IReader = DividendsCsvReader(fileName, parseDateFormat, parseDelimiter)

        self._dividends = reader.read()

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

    def __outputDividends(self) -> None:
        dividendsWriter: IWriter = DividendsConsoleWriter()
        dividendsSummaryWriter: IWriter = DividentsSummaryConsoleWriter()

        dividendsWriter.write(self._dividends)
        dividendsSummaryWriter.write(self._dividends)


DividendsExchangeCalculator().main()