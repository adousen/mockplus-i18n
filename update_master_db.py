# -*- coding: utf-8 -*-
import sqlite3
import urllib

def update_en(key, en):
    print key, en
    conn = sqlite3.connect('./master.db')
    cur = conn.cursor()
    cur.execute('UPDATE master SET en_value = ? WHERE key = ?', (en, key))
    conn.commit()


def update_master():
    with open('./en.txt', 'r') as f:
        line = f.readline()
        while line:
            s = line.split('=')
            k, v = s
            key = 'Back_' + k.strip()
            en =  v.strip()[1:-1]
            update_en(key, urllib.quote_plus(en))
            line = f.readline()


if __name__ == '__main__':
    update_master()
