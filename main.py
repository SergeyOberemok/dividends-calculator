from DividendsExchangeCalculator import DividendsExchangeCalculator
from domain.files.filesPaths import findFilesPath
from domain.models.dividend import Dividend
from domain.services.dividendsReader import DividendsCsvReader
from domain.services.dividendsWriter import DividendsConsoleWriter, DividendsSummaryConsoleWriter


def askForTaxPercentage() -> int:
    defaultTaxPercentage: int = 19

    taxPercentageAnswer = input(
        f"Enter tax percentage (default {defaultTaxPercentage}) "
    )
    return (
        defaultTaxPercentage
        if taxPercentageAnswer == ""
        else int(taxPercentageAnswer)
    )


def askForDoFetchExchangeRate() -> bool:
    return (
        True if input("Fetch exchange rate [y/N] ") == "y" else False
    )


def fetchDividends(file_name: str) -> list[Dividend]:
    parseDateFormat: str = "%Y%m%d"
    parseDelimiter: str = ","
    result = DividendsCsvReader(file_name, parseDateFormat, parseDelimiter).read()

    return result


def main():
    taxPercentage = askForTaxPercentage()
    doFetchExchangeRate = askForDoFetchExchangeRate()
    fileNames = findFilesPath('csv')

    for fileName in fileNames:
        dividends = fetchDividends(fileName)

        dividends = DividendsExchangeCalculator(taxPercentage, doFetchExchangeRate).main(dividends)

        DividendsConsoleWriter().write(dividends)
        DividendsSummaryConsoleWriter().write(dividends)


if __name__ == '__main__':
    main()
