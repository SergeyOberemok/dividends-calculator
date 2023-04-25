
from abc import ABC, abstractmethod
import csv
from ..helpers.dates import parseDate
from ..models.dividend import Dividend, DividendFactory


class IReader(ABC):
    @abstractmethod
    def read(self) -> list:
        pass


class DividendsCsvReader(IReader):
    _path: str
    _parsingDateFormat: str
    _delimiter: str

    def __init__(self, path: str, parsingDateFormat: str, delimiter: str) -> None:
        self._path = path
        self._parsingDateFormat = parsingDateFormat
        self._delimiter = delimiter

    def read(self) -> list[Dividend]:
        dividends = []

        with open(self._path) as file:
            reader = csv.reader(file, delimiter=self._delimiter)

            for data in reader:
                if self.__isDividendRecord(data):
                    params = self.__formParams(data)
                    dividend = DividendFactory.create(params)
                    dividends.append(dividend)

        return dividends

    def __isDividendRecord(self, data) -> bool:
        return (
            True
            if data[0] == "DividendDetail"
            and data[1] == "Data"
            and data[2] == "Summary"
            else False
        )

    def __formParams(self, data: list[str]) -> dict:
        (
            _,
            _,
            _,
            currency,
            symbol,
            _,
            country,
            reportDate,
            _,
            shares,
            _,
            _,
            gross,
            _,
            grossInUSD,
            withhold,
            _,
            withholdInUSD,
            _,
        ) = data
        reportDate = parseDate(reportDate, self._parsingDateFormat)

        payments = [dict(currency=currency, gross=gross, withhold=withhold)]

        if currency.upper() != "USD":
            payments.append(
                dict(currency="USD", gross=grossInUSD, withhold=withholdInUSD)
            )

        return dict(
            currency=currency,
            symbol=symbol,
            country=country,
            reportDate=reportDate,
            shares=shares,
            payments=payments,
        )
