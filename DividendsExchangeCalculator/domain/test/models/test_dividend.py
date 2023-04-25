
import pytest
from ...models.dividend import Dividend
from datetime import datetime
from ...helpers.dates import toDateStringISO


def test_dividend() -> None:
    reportDate = datetime(2023, 4, 25)
    shares = 2

    dividend = Dividend('', '', '', toDateStringISO(reportDate), str(shares), [])

    assert dividend.dateOfEarning == reportDate
    assert dividend.quantity == shares
    assert dividend.prevWorkingDateBeforePaid != reportDate

@pytest.fixture
def dividendMock() -> Dividend:
    return Dividend('', '', '', datetime.now(), 0, [])

def test_prevWorkingDateBeforePaid(dividendMock) -> None:
    reportDate = dividendMock.dateOfEarning = datetime(2023, 4, 25)

    assert dividendMock.prevWorkingDateBeforePaid != reportDate
    assert dividendMock.prevWorkingDateBeforePaid == datetime(2023, 4, 24)
