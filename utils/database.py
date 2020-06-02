import argparse
import os
import sqlite3


def create_db(args):
    db = args.database
    table_name = args.table_name
    if os.path.isfile(db):
        delete = input(f"Database {db} already exists." "Overwrite [yes,y \ no, n] ?")
        if delete in ("yes", "y"):
            os.remove(db)
        else:
            print("Try again with other database name")
            exit()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = f"CREATE TABLE {table_name} (buy int, sell int, dt datetime)"
    c.execute(query)
    conn.commit()
    conn.close()
    print("Table created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DB helper for money tracker")
    parser.add_argument(
        "-d", "--database", type=str, help="Name of the sqlite database file"
    )
    parser.add_argument(
        "-t",
        "--table-name",
        dest="table_name",
        type=str,
        help="Name of the table you want to create. For example itau.",
    )
    args = parser.parse_args()
    create_db(args)
