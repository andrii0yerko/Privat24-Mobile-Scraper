from datetime import datetime

from bs4 import BeautifulSoup

from pb24exporter.record import Record


class TransactionPage:
    def __init__(self, driver):
        self.driver = driver

    def scrape(self):
        bs = BeautifulSoup(self.driver.page_source, features="xml")
        return self._parse_record(bs)

    def back(self):
        self.driver.back()

    def _parse_record(self, bs: BeautifulSoup):
        # it also can be done without bs
        # TODO: research
        tv_name: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvTitle"})["text"]
        tv_sum: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvSum"})["text"]
        tv_description: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvDescription"})["text"]
        tv_date: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvDate"})["text"]
        tv_id = bs.find_all("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvValue"})[-1]["text"]

        amount, currency = self._preprocess_tvsum(tv_sum)
        date = self._preprocess_tvdate(tv_date)
        return Record(
            date=date,
            amount=amount,
            currency=currency,
            description=tv_description,
            category=tv_name,
            uid=tv_id,
        )

    def _preprocess_tvsum(self, tvsum: str) -> tuple[float, str]:
        tvsum = tvsum.replace("\xa0", " ")
        amount, currency = tvsum.rsplit(" ", 1)
        amount = float(amount.replace(",", ".").replace(" ", ""))
        return amount, currency

    def _preprocess_tvdate(self, tvdate: str) -> datetime:
        return datetime.strptime(tvdate, "%d.%m.%Y %H:%M:%S")
