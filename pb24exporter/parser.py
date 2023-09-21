import time
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy
from bs4 import BeautifulSoup

import pb24exporter.settings as settings
from pb24exporter.record import Record


def preprocess_tvsum(tvsum: str) -> tuple[float, str]:
    tvsum = tvsum.replace("\xa0", " ")
    amount, currency = tvsum.rsplit(" ", 1)
    amount = float(amount.replace(",", ".").replace(" ", ""))
    return amount, currency


def preprocess_tvdate(tvdate: str) -> datetime:
    return datetime.strptime(tvdate, "%d.%m.%Y %H:%M:%S")


class ConsecutiveDeduplication:
    def __init__(self):
        self.prev = None

    def is_new(self, rec: Record) -> bool:
        if self.prev is None:
            self.prev = rec
            return True

        if self.prev.uid == rec.uid:
            return False

        self.prev = rec
        return True


class Parser:
    def __init__(self, driver, deduplication=None):
        self.driver = driver
        self.deduplication = deduplication or ConsecutiveDeduplication()

    def check_if_loaded(self):
        return self.driver.current_activity == settings.MAIN_ACTIVITY

    def parse(self):
        driver = self.driver

        while True:
            records = self._find_records()
            num_records = len(records)

            ys, heights = [], []
            for rec in records:
                rect = rec.rect
                heights.append(rect["height"])
                ys.append(rect["y"])

            for i in range(num_records):
                # required because of object staling in appium
                records = self._find_records()
                record = records[i]
                record.click()

                time.sleep(settings.PARSING_TIMEOUT_S)
                bs = BeautifulSoup(driver.page_source, features="xml")
                rec = self._parse_record(bs)
                driver.back()

                if self.deduplication.is_new(rec):
                    yield rec

                # TODO: Handle end of history

            y_to = ys[0]
            y_from = ys[-1] + heights[-1]
            driver.swipe(0, y_from, 0, y_to, settings.SWIPE_DURATION_MS)

    def _parse_record(self, bs: BeautifulSoup):
        tv_name: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvTitle"})["text"]
        tv_sum: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvSum"})["text"]
        tv_description: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvDescription"})["text"]
        tv_date: str = bs.find("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvDate"})["text"]
        tv_id = bs.find_all("android.widget.TextView", {"resource-id": "ua.privatbank.ap24:id/tvValue"})[-1]["text"]

        amount, currency = preprocess_tvsum(tv_sum)
        date = preprocess_tvdate(tv_date)
        return Record(
            date=date,
            amount=amount,
            currency=currency,
            description=tv_description,
            category=tv_name,
            uid=tv_id,
        )

    def _find_records(self):
        return self.driver.find_elements(AppiumBy.XPATH, "//android.widget.RelativeLayout[@clickable='true']")
