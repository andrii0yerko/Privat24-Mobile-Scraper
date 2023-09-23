import appium.webdriver
import click
from appium.options.android.uiautomator2.base import UiAutomator2Options

from pb24exporter.exporters.factory import create_exporter
from pb24exporter.scraper import Scraper


def call_for_login(parser):
    while not parser.check_if_loaded():
        click.echo("Please open Privat24 app and login first")
        click.pause()


@click.command()
@click.option("--end-date", default=None, type=click.DateTime(), help="Date to stop scraping at", show_default=True)
@click.option("--export-format", type=click.Choice(["xlsx"]), default="xlsx", help="Format for the exported data", show_default=True)
@click.option("--export-path", default="transaction-history.xlsx", help="Path to the exported file", show_default=True)
@click.option(
    "--appium-server-url",
    envvar="APPIUM_SERVER_URL",
    default="http://localhost:4723",
    help="URL of the Appium server. If not present, will be taken from APPIUM_SERVER_URL environmental variable",
    show_default=True,
)
def main(end_date, export_format, export_path, appium_server_url):
    driver = appium.webdriver.Remote(  # type: ignore
        command_executor=appium_server_url,
        options=UiAutomator2Options().load_capabilities(
            dict(
                platformName="Android",
                automationName="uiautomator2",
                newCommandTimeout=0,
            )
        ),
    )

    save_strategy = create_exporter(format=export_format, path=export_path)
    scraper = Scraper(driver)
    call_for_login(scraper)

    for i, rec in enumerate(scraper.scrape()):
        if rec.date < end_date:
            click.echo("Reached end date")
            break
        save_strategy.save(rec)

    save_strategy.flush()
    save_strategy.close()
