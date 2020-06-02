import os
import time

import click
from rich import print
from dotenv import load_dotenv  # pylint: disable=import-error

from collector import collector, fetch
from plot import plot

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
ITAU = os.getenv("ITAU_URL")
BROU = os.getenv("BROU_URL")

@click.group()
def main():
    """CLI for monitoring exchange rate"""


@main.command(help="Updates exchage rate and returns real time value")
def query():
    print("Updating info for Itaú :bank: ...")
    itau_collector = collector.DataCollector(DB_NAME, "itau", ITAU, fetch.itau_fetch)
    itau_collector.update()
    print("Updating info for BROU :bank: ...")
    brou_collector = collector.DataCollector(DB_NAME, "brou", BROU, fetch.brou_fetch)
    brou_collector.update()

@main.command(help="Plots historic rate for the day")
@click.argument('day', required=True, type=str)
@click.argument('bank', required=True, type=str)
def daily(day, bank):
    plotter = plot.DataPlotter(DB_NAME, bank.lower())
    try:
        plotter.plot_day(day)
    except IndexError:
        print("I don't have data for that day :cry:")

@main.command(help="Plots historic rate for the week")
@click.argument('day', required=True, type=str)
@click.argument('bank', required=True, type=str)
def weekly(day, bank):
    plotter = plot.DataPlotter(DB_NAME, bank.lower())
    try:
        plotter.plot_week(day)
    except IndexError:
        print("I don't have data for that week :cry:")


if __name__ == "__main__":
    main()
