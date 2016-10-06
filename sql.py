import sqlite3

with sqlite3.connect("messages.db") as connection:
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages(name TEXT, email TEXT, message TEXT)""")
