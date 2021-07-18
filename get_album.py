import sqlite3 as sl
import random 

con = sl.connect('my_data.db', check_same_thread=False)
c = con.cursor()


def get_next_by_date(tg_id):
    c.execute("SELECT * FROM actions WHERE tg_id=?", (tg_id,))
    listened = [i[1] for i in c.fetchall()]
    c.execute("SELECT * FROM albums")
    all_albums = c.fetchall()
    remaining = []
    for i in all_albums:
        if i[0] not in listened:
            remaining.append(i)
    if not remaining:
        return None
    return remaining[0]


def get_next_by_alph(tg_id):
    c.execute("SELECT * FROM actions WHERE tg_id=?", (tg_id,))
    listened = [i[1] for i in c.fetchall()]
    c.execute("SELECT * FROM albums")
    all_albums = c.fetchall()
    remaining = []
    for i in all_albums:
        if i[0] not in listened:
            remaining.append(i)
    if not remaining:
        return None
    return min(remaining)


def get_next_by_rand(tg_id):
    c.execute("SELECT * FROM actions WHERE tg_id=?", (tg_id,))
    listened = [i[1] for i in c.fetchall()]
    c.execute("SELECT * FROM albums")
    all_albums = c.fetchall()
    remaining = []
    for i in all_albums:
        if i[0] not in listened:
            remaining.append(i)
    if not remaining:
        return None
    return remaining[random.randint(0, len(remaining) - 1)]
