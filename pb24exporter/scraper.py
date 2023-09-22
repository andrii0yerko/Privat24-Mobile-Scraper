import time

import pb24exporter.settings as settings
from pb24exporter.pages import TransactionHistoryPage
from pb24exporter.pages.transaction import TransactionPage
from pb24exporter.record import Record


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


class Scraper:
    def __init__(self, driver, deduplication=None):
        self.driver = driver
        self.deduplication = deduplication or ConsecutiveDeduplication()

    def check_if_loaded(self):
        return self.driver.current_activity == settings.MAIN_ACTIVITY

    def scrape(self):
        history_page = TransactionHistoryPage(self.driver)

        while True:
            for i in range(history_page.num_records):
                # required because of object staling in appium
                history_page.click_record(i)

                time.sleep(settings.PARSING_TIMEOUT_S)
                transaction_page = TransactionPage(self.driver)
                rec = transaction_page.scrape()
                transaction_page.back()

                if self.deduplication.is_new(rec):
                    yield rec

                # TODO: Handle end of history

            history_page.scroll()
