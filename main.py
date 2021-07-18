import telebot
from telebot import types
import sqlite3 as sl
from get_album import get_next_by_alph, get_next_by_date, get_next_by_rand
from spotify_api import SpotifyAPI
from search_api import get_reviews

API_KEY = "API_KEY"
bot = telebot.TeleBot(API_KEY)
spotify = SpotifyAPI('Client ID', 'Client Secret')

con = sl.connect('my_data.db', check_same_thread=False)
c = con.cursor()

greeting = """
Welcome to 1001 Albums You Must Hear Before You Die  \n
Here you can find every album from one of the most famous almanac in music history and brief reviews from musical critics \n
In which order do you prefer to start listen them?
"""


@bot.message_handler(commands=["start"])
def send_start_info(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Chronological', callback_data='setup/chrono'))
    keyboard.add(types.InlineKeyboardButton(text='Alphabetical', callback_data='setup/alpha'))
    keyboard.add(types.InlineKeyboardButton(text='Random', callback_data='setup/random'))
    bot.send_message(message.chat.id, greeting, reply_markup=keyboard)


@bot.message_handler(commands=["stats"])
def send_stats_info(message):
    tg_id = message.from_user.id
    c.execute("SELECT * FROM actions WHERE tg_id=?", (tg_id,))
    listened = c.fetchall()
    info = f"""You have listened {len(listened)} albums out of 1047 \nProgress: {round(len(listened) * 100 / 1047, 2)}%"""
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=["next"])
def send_next_album(message):
    tg_id = message.from_user.id
    c.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
    l_type = c.fetchone()[1]
    if l_type == 1:
        album = get_next_by_date(tg_id)
    elif l_type == 2:
        album = get_next_by_alph(tg_id)
    else:
        album = get_next_by_rand(tg_id)

    if album is None:
        bot.send_message(message.chat.id, "Congrats you listened every album from almanac!")
    else:
        try:
            link = spotify.get_album(album[0])
        except:
            link = "We can't find this album on spotify :("
        msg = f"{album[0]}, {album[1]}\n\n{link}"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Listened', callback_data=f'listened/{album[0]}'))
        keyboard.add(types.InlineKeyboardButton(text='Reviews', callback_data=f'review/{album[0]}'))
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def check_callback(call):
    print(call.message.chat.id)
    if call.data[:6] == "setup/":
        if call.data == "setup/chrono":
            t = 1
        elif call.data == "setup/alpha":
            t = 2
        else:
            t = 3

        c.execute("SELECT * FROM users WHERE tg_id=?", (call.from_user.id,))
        if not c.fetchall():
            c.execute("INSERT INTO users (tg_id, type) values(?, ?)", (call.from_user.id, t))
            con.commit()
        else:
            c.execute("UPDATE users SET type = ? WHERE tg_id=?", (t, call.from_user.id))
            con.commit()
        bot.answer_callback_query(callback_query_id=call.id, text='Perfect choice!')

    if call.data[:9] == "listened/":
        album = call.data[9:]
        c.execute("INSERT INTO actions (tg_id, name) values(?, ?)", (call.from_user.id, album))
        con.commit()

    if call.data[:7] == "review/":
        reviews = get_reviews(call.data[7:])
        keyboard = types.InlineKeyboardMarkup()
        for i in reviews:
            keyboard.add(types.InlineKeyboardButton(text=i[0], url=i[1]))
        bot.send_message(call.message.chat.id, "Here are some reviews:", reply_markup=keyboard)


bot.polling()
