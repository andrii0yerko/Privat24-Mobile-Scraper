from appium.webdriver.common.appiumby import AppiumBy

from pb24exporter import settings


class TransactionPageLocators:
    RECORDS = (AppiumBy.XPATH, "//android.widget.RelativeLayout[@clickable='true']")


# TODO Handle selenium.common.exceptions: NoSuchElementException, StaleElementReferenceException
class TransactionHistoryPage:
    def __init__(self, driver):
        self.driver = driver

    def click_record(self, index):
        # required because of object staling in appium
        records = self._find_records()
        record = records[index]
        record.click()

    @property
    def num_records(self):
        return len(self._find_records())

    def show_next(self):
        records = self._find_records()

        ys, heights = [], []
        for rec in records:
            rect = rec.rect
            heights.append(rect["height"])
            ys.append(rect["y"])

        y_to = ys[0]
        y_from = ys[-1] + heights[-1]
        self.driver.swipe(0, y_from, 0, y_to, settings.SWIPE_DURATION_MS)

    def _find_records(self):
        return self.driver.find_elements(*TransactionPageLocators.RECORDS)
