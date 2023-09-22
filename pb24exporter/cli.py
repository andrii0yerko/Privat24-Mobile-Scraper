import appium.webdriver
import click
from appium.options.android.uiautomator2.base import UiAutomator2Options

from pb24exporter.scraper import Scraper


def call_for_login(parser):
    while not parser.check_if_loaded():
        click.echo("Please open Privat24 app and login first")
        click.pause()


@click.command()
@click.option("--appium-server-url", envvar="APPIUM_SERVER_URL")
def main(appium_server_url):
    driver = appium.webdriver.Remote(
        command_executor=appium_server_url,
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
