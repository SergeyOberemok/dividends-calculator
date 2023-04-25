
from abc import ABC, abstractmethod
from ..models.dividend import Dividend
from itertools import chain
from functools import reduce


class IWriter(ABC):
    @abstractmethod
    def write(self, dividends: list[Dividend]) -> bool:
        pass


class DividendsConsoleWriter(IWriter):
    def write(self, dividends: list[Dividend]) -> bool:
        for dividend in dividends:
            print(str(dividend))

        return True

class DividentsSummaryConsoleWriter(IWriter):
    def write(self, dividents: list[Dividend]) -> bool:
        print(self.__getSummary(dividents))

        return True

    def __getSummary(self, dividents: list[Dividend]) -> str:
        listOfSummaries = [*(dividend.getSummary() for dividend in dividents)]
        summaries = list(chain(*listOfSummaries))
        currencies = []

        for summary in summaries:
            if summary['currency'] not in currencies:
                currencies.append(summary['currency'])

        result = f"""Dividends are {len(dividents)}. Currencies are {len(currencies)}
"""

        for currency in currencies:
            filtered = [*filter(lambda summary: summary['currency'] == currency, summaries)]

            gross = reduce(lambda acc, summary: acc + summary['gross'], filtered, 0)
            withhold = reduce(lambda acc, summary: acc + summary['withhold'], filtered, 0)
            earned = reduce(lambda acc, summary: acc + summary['earned'], filtered, 0)
            taxToPay = reduce(lambda acc, summary: acc + summary['taxToPay'], filtered, 0)

            result += f"""Total for currency {currency} earned is {round(earned, 2)} where gross is {round(gross, 2)} withhold is {round(withhold, 2)} and tax to pay {round(taxToPay, 2)}
"""
        return result