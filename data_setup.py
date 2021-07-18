import sqlite3 as sl
con = sl.connect('my_data.db')
c = con.cursor()

with con:
    c.execute("""
        CREATE TABLE users (
            tg_id text,
            type integer
        );
    """)

with con:
    c.execute("""
        CREATE TABLE albums (
            name text,
            year integer
        );
    """)

with con:
    c.execute("""
        CREATE TABLE actions (
            tg_id text,
            name text
        );
    """)