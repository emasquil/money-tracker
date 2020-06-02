import sqlite3

import pandas as pd
from rich.console import Console
import termplotlib as tpl
import numpy as np


class DataPlotter:
    def __init__(self, db: str, table_name: str):
        self.db = db
        self.table_name = table_name

    def _get_data(self, min_date, max_date):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        query = f'SELECT * from {self.table_name} where dt>="{min_date}" and dt<="{max_date}" order by dt'
        data = c.execute(query).fetchall()
        x = [float((d[0] + d[1]) / 200) for d in data]
        y = [d[2] for d in data]
        df = pd.DataFrame(x, index=pd.to_datetime(y))
        return df

    def plot_day(self, day):
        console = Console()
        max_date = pd.to_datetime(day) + pd.Timedelta("23 hours")
        min_date = pd.to_datetime(day)
        data = self._get_data(min_date, max_date)
        console.print("Raw data", style="bold magenta")
        console.print(data)
        idx = pd.date_range(data.index[0], periods=24, freq="H")
        data = data.reindex(idx, method="nearest")
        x = [d for d in range(24)]
        y = np.array([float(d) for d in data.values])
        fig = tpl.figure()
        fig.plot(
            x=x,
            y=y,
            width=50,
            height=15,
            ylim=(min(y - 0.5), max(y + 0.5)),
            label=self.table_name.capitalize(),
            title=f'Day {day}',
            xlim=(0, 24),
        )
        console.print(fig.get_string(), style="bold magenta")

    def plot_week(self, day):
        console = Console()
        max_date = pd.to_datetime(day) + pd.Timedelta("23 hours")
        min_date = pd.to_datetime(day) - pd.Timedelta("6 days")
        data = self._get_data(min_date, max_date)
        console.print("Raw data", style="bold magenta")
        console.print(data)
        idx = pd.date_range(end=max_date, periods=7, freq="D")
        data = data.reindex(idx, method="ffill").bfill()
        x = [d for d in range(7)]
        y = np.array([float(d) for d in data.values])
        fig = tpl.figure()
        fig.plot(
            x=x,
            y=y,
            width=50,
            height=15,
            ylim=(min(y - 0.1), max(y + 0.1)),
            label=self.table_name.capitalize(),
            title=f'Week ending {day}',
            xlim=(0, 7),
        )
        console.print(fig.get_string(), style="bold magenta")
