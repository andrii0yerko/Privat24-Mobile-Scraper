import logging

import appium.webdriver
import click
from appium.options.android.uiautomator2.base import UiAutomator2Options

from pb24exporter.exporters.factory import create_exporter
from pb24exporter.main import main_loop
from pb24exporter.scraper import TransactionScraper


def call_for_action_callback(msg):
    click.echo(msg)
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
def cli(end_date, export_format, export_path, appium_server_url):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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
    scraper = TransactionScraper(driver, call_for_action_callback=call_for_action_callback)

    main_loop(scraper, save_strategy, lambda rec: rec.date < end_date)
