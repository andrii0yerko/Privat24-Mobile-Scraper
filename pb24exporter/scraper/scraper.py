import time

import pb24exporter.settings as settings
from pb24exporter.record import Record
from pb24exporter.scraper.pages import TransactionHistoryPage, TransactionPage


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


class TransactionScraper:
    def __init__(self, driver, call_for_action_callback, deduplication=None):
        self._driver = driver
        self._call_for_action_callback = call_for_action_callback
        self._deduplication = deduplication or ConsecutiveDeduplication()

    def scrape(self):
        self._wait_until_loaded()

        history_page = TransactionHistoryPage(self._driver)

        while True:
            yield from filter(self._deduplication.is_new, self._scrape_screen(history_page))
            # TODO: Handle end of history

            history_page.show_next()

    def _scrape_screen(self, history_page):
        for i in range(history_page.num_records):
            # required because of object staling in appium
            history_page.click_record(i)

            time.sleep(settings.PARSING_TIMEOUT_S)
            transaction_page = TransactionPage(self._driver)
            rec = transaction_page.scrape()
            transaction_page.back()
            yield rec

    def _wait_until_loaded(self):
        while True:
            if self._driver.current_activity == settings.MAIN_ACTIVITY:
                return
            self._call_for_action_callback("Please open Privat24 app and login first")
