#!/usr/bin/env python3

import sqlite3
import os

DATABASE_FILE = 'website.sqlite3'

def reset_database():
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute('''CREATE TABLE users (
    id INT,
    username VARCHAR(50),
    password VARCHAR(50),
    signed_up DATE,
    privileges  VARCHAR(50)
    )''')

    users_entries = [
        [1, 'administrator', 'nobody_knows', '1970-01-01', 'all'],
        [23, 'bob', 'bob$passw0rd',  '2011-05-02', 'user'],
        [42, 'alice', 'verysecret',  '2012-06-04', 'user'],
        [80, 'heinz', 'n1xd0rf', '2013-02-03', 'user'],
    ]

    connection.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?)', users_entries)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    reset_database()
