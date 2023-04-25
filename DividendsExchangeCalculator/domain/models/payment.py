
from ..helpers.numbers import parseFloat, exchange

class Payment:
    taxPercentage: int

    _currency: str
    _gross: float
    _withhold: float
    _exchangeRate: float

    def __init__(self, currency, gross, withhold, exchangeRate: float = 1, isTaxRelief = lambda: False) -> None:
        self._currency = currency
        self.gross = gross
        self.withhold = withhold
        self.exchangeRate = exchangeRate
        self._isTaxRelief = isTaxRelief

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def gross(self) -> float:
        return self._gross

    @gross.setter
    def gross(self, value) -> None:
        self._gross = parseFloat(value)

    @property
    def withhold(self) -> float:
        return self._withhold

    @withhold.setter
    def withhold(self, value) -> None:
        self._withhold = abs(parseFloat(value))

    @property
    def exchangeRate(self) -> float:
        return self._exchangeRate

    @exchangeRate.setter
    def exchangeRate(self, value) -> None:
        self._exchangeRate = parseFloat(value)

    @property
    def isTaxRelief(self) -> bool:
        return self._isTaxRelief()

    @isTaxRelief.setter
    def isTaxRelief(self, value) -> None:
        self._isTaxRelief = value

    @property
    def earned(self) -> float:
        return round(self._gross - self._withhold, 2)

    @property
    def paidTaxPercentage(self) -> int:
        if self._withhold == 0:
            return 0

        return round(self._withhold / self._gross * 100)

    @property
    def taxPercentageToPay(self) -> int:
        if self._isTaxRelief:
            taxPercentage = Payment.taxPercentage - self.paidTaxPercentage

            return taxPercentage if taxPercentage > 0 else 0

        return Payment.taxPercentage

    @property
    def taxToPay(self) -> float:
        return round(self._gross * self.taxPercentageToPay / 100, 2)

    def getSummary(self) -> dict:
        return {
            'currency': self._currency,
            'gross': self._gross,
            'withhold': self._withhold,
            'earned': self.earned,
            'taxToPay': self.taxToPay,
            }

    def __str__(self) -> str:
        return f"""Earned {self.earned} {self.currency} = gross {self.gross} minus withhold {self.withhold} ({self.paidTaxPercentage}%). To pay {self.taxToPay} ({self.taxPercentageToPay}%). Exchange rate was {self.exchangeRate}
"""


class PaymentFactory:
    
    def create(currency: str, gross, withhold, exchangeRate) -> Payment:
        gross = parseFloat(gross)
        withhold = parseFloat(withhold)
        exchangeRate = parseFloat(exchangeRate)

        if exchangeRate > 0:
            gross = exchange(gross, exchangeRate)
            withhold = exchange(withhold, exchangeRate)

        return Payment(currency, gross, withhold, exchangeRate)