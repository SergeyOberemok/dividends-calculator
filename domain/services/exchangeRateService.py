
import requests
from datetime import datetime
from ..helpers.dates import toDateStringISO
from ..helpers.numbers import parseFloat


class ExchangeRateService:
    _url: str = "http://api.nbp.pl/api/exchangerates/rates/a/%s/%s?format=json"

    def fetchAverageExchangeRate(self, currency: str, date: datetime) -> float:
        url = self._url % (currency, toDateStringISO(date))

        try:
            response = requests.get(url).json()
            return parseFloat(response["rates"][0]["mid"])
        except:
            return 0
