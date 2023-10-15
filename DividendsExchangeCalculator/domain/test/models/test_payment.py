import pytest
from ...models.payment import Payment, PaymentFactory


def test_payment() -> None:
    currency, gross, withhold, exchangeRate = "usd", 125, 25, 4.44

    payment = Payment(currency, str(gross), str(withhold), exchangeRate)

    assert payment.currency == currency
    assert payment.gross == gross
    assert payment.withhold == withhold
    assert payment.exchangeRate == exchangeRate


def test_paymentFactory() -> None:
    gross, withhold, exchangeRate = 1, 0.2, 4.25

    payment = PaymentFactory.create("", str(gross), str(withhold), str(exchangeRate))

    assert payment.gross == round(gross * exchangeRate, 2)
    assert payment.withhold == round(withhold * exchangeRate, 2)


@pytest.fixture
def getIsTaxRelief():
    return lambda: True


@pytest.fixture
def paymentMock(getIsTaxRelief=lambda: False) -> Payment:
    return Payment("", 0, 0, isTaxRelief=getIsTaxRelief)


def test_earned(paymentMock) -> None:
    gross = paymentMock.gross = 4
    withhold = paymentMock.withhold = 2

    assert paymentMock.earned == gross - withhold


@pytest.fixture
def grossAndWithholdMockList() -> list:
    return [(4, 2, 50), (4, 0, 0), (0.5, 0.1, 20)]


def test_paidTaxPercentage(paymentMock, grossAndWithholdMockList) -> None:
    for gross, withhold, answer in grossAndWithholdMockList:
        paymentMock.gross = gross
        paymentMock.withhold = withhold

        assert paymentMock.paidTaxPercentage == answer


def test_defaultTaxPercentageToPay(paymentMock) -> None:
    taxPercentage = Payment.taxPercentage = 10

    assert paymentMock.taxPercentageToPay == taxPercentage


def test_taxPercentageToPay(getIsTaxRelief, paymentMock) -> None:
    gross = paymentMock.gross = 100
    withhold = paymentMock.withhold = 10
    taxPercentage = Payment.taxPercentage = 15

    assert paymentMock.taxPercentageToPay < taxPercentage
    assert paymentMock.taxPercentageToPay == taxPercentage - (gross * withhold / 100)


def test_taxToPay(paymentMock) -> None:
    gross = paymentMock.gross = 200
    withhold = paymentMock.withhold = 10
    taxPercentage = Payment.taxPercentage = 25

    assert paymentMock.taxToPay == 200 * 25 / 100 - withhold
