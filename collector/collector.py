from datetime import datetime
from typing import Callable
import sqlite3
from rich import print

class DataCollector:
    def __init__(self, db: str, table_name: str, url: str, fetch_function: Callable):
        self.db = db
        self.table_name = table_name
        self.url = url
        self.fetch_function = fetch_function

    def _insert(self, buy, sell, dt):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        query = f"INSERT into {self.table_name} VALUES({buy},{sell},'{dt}')"
        c.execute(query)
        conn.commit()
        conn.close()

    def _update_msg(self, old_mean, new_mean):
        change = ":no_entry:"
        if new_mean > old_mean:
            change = f":arrow_up: ({new_mean - old_mean})"
        elif new_mean < old_mean:
            change = f":arrow_down: ({new_mean - old_mean})"
        print(f"Current mean in {self.table_name.capitalize()} is $UYU {new_mean} {change}")

    def update(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        query = f"SELECT buy,sell FROM {self.table_name} ORDER BY dt desc"
        c.execute(query)
        try:
            old_buy, old_sell = c.fetchone()
        except TypeError:
            # When running the first time the table is empty
            old_buy, old_sell = (0, 0)
        conn.close()
        new_buy, new_sell = self.fetch_function(self.url)
        if (new_buy != old_buy) or (new_sell != old_sell):
            self._insert(new_buy, new_sell, str(datetime.now()))
        old_mean = (old_buy + old_sell) / (2 * 100)
        mean = (new_buy + new_sell) / (2 * 100)
        self._update_msg(old_mean, mean)
