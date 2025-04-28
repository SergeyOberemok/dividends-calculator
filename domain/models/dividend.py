
from datetime import datetime
from ..helpers.dates import toDateStringISO, printDay, parseISODate, getWorkingDayBefore
from ..helpers.numbers import parseInt
from .payment import Payment
from .country import Country


class Dividend:
    _currency: str
    _symbol: str
    _country: Country
    _dateOfEarning: datetime
    _quantity: int
    _payments: list[Payment]

    def __init__(
        self,
        currency: str,
        symbol: str,
        country,
        reportDate,
        shares,
        payments: list[Payment],
    ) -> None:
        self._currency = currency
        self._symbol = symbol
        self.country = country
        self.dateOfEarning = reportDate
        self.quantity = shares
        self.payments = payments

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def country(self) -> str:
        return str(self._country)

    @country.setter
    def country(self, value) -> None:
        if isinstance(value, str):
            value = Country(value)
        self._country = value

    @property
    def dateOfEarning(self) -> datetime:
        return self._dateOfEarning

    @dateOfEarning.setter
    def dateOfEarning(self, value) -> None:
        if isinstance(value, str):
            value = parseISODate(value)
        self._dateOfEarning = value

    @property
    def prevWorkingDateBeforePaid(self) -> datetime:
        return getWorkingDayBefore(self._dateOfEarning)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value) -> None:
        self._quantity = parseInt(value)

    @property
    def payments(self) -> list[Payment]:
        return self._payments

    @payments.setter
    def payments(self, value: list[Payment]) -> None:
        self._payments = value

        for payment in self._payments:
            payment.isTaxRelief = lambda: self.isTaxRelief

    @property
    def isTaxRelief(self) -> bool:
        return self._country.isTaxRelief

    def getSummary(self) -> list:
        return [*(payment.getSummary() for payment in self.payments)]

    def getPaymentByCurrency(self, currency: str) -> Payment:
        return next((payment for payment in self._payments if payment.currency == currency), None)

    def __str__(self) -> str:
        payments = "".join(str(payment) for payment in self.payments)

        return f"""
Symbol {self.symbol} from country {self.country} of currency {self.currency} on {printDay(self.dateOfEarning)} {toDateStringISO(self.dateOfEarning)}
Earnings on {printDay(self.prevWorkingDateBeforePaid)} {toDateStringISO(self.prevWorkingDateBeforePaid)} were:
{payments}
"""


class DividendFactory:
    def create(dividendParams: dict) -> Dividend:
        payments: list[Payment] = []

        for paymentParams in dividendParams["payments"]:
            payment = Payment(
                paymentParams["currency"],
                paymentParams["gross"],
                paymentParams["withhold"],
            )
            payments.append(payment)

        return Dividend(
            dividendParams["currency"],
            dividendParams["symbol"],
            dividendParams["country"],
            dividendParams["reportDate"],
            dividendParams["shares"],
            payments,
        )
