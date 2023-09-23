import typing

from pb24exporter.record import Record


class ScraperStrategy(typing.Protocol):
    def scrape(self) -> typing.Generator[Record, None, None]:
        ...


class ExporterStrategy(typing.Protocol):
    def save(self, rec: Record) -> None:
        ...

    def flush(self) -> None:
        ...

    def close(self) -> None:
        ...


def main_loop(scraper: ScraperStrategy, exporter: ExporterStrategy, stop_condition):
    """Main function of the application.

    Args:
        scraper (TransactionScraper): Scraper instance.
        exporter (BaseExporter): Exporter instance.
        stop_condition (function): Stop condition function.
    """

    for transaction in scraper.scrape():
        if stop_condition(transaction):
            break
        exporter.save(transaction)

    exporter.flush()
    exporter.close()
