import os

import appium.webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from dotenv import load_dotenv

from pb24exporter.scraper import Scraper


def call_for_login(parser):
    while not parser.check_if_loaded():
        print("Please open Privat24 app and login")
        input("Press any key to continue...")


def main():
    load_dotenv()

    driver = appium.webdriver.Remote(
        command_executor=os.environ["APPIUM_SERVER_URL"],
        options=UiAutomator2Options().load_capabilities(
            dict(
                platformName="Android",
                automationName="uiautomator2",
                newCommandTimeout=0,
            )
        ),
    )

    scraper = Scraper(driver)
    call_for_login(scraper)

    for i, rec in enumerate(scraper.scrape()):
        print(i, rec)
        if i == 25:
            break
