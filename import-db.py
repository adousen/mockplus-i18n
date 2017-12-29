# -*- coding: utf-8 -*-
import sqlite3
import os
from os.path import join
from dbHelper import get_conn_and_cursor
import urllib
import chardet


def insert_img(img_data):
    '''
    插入图片
    '''
    (master_key, img_path) = img_data
    conn, cur = get_conn_and_cursor()
    sql = r'''
        INSERT INTO img (
            master_key, img, addtime, state
        )
        VALUES (
            %s, %s, now(), 0
        )
        '''
    cur.execute(sql, (master_key, img_path))
    conn.commit()


def insert_str(data):
    '''
    插入中英文翻译内容
    '''
    (key, en, zh) = data
    conn, cur = get_conn_and_cursor()
    sql = r'''
    INSERT INTO strs(
        master_key, en, cn, jp, addtime, state
    )
    VALUES (
        %s, %s, %s, '', now(), 0
    )
    '''
    cur.execute(sql, (key, en, zh))
    conn.commit()


def update_jp(key, jp):
    '''
    更新日文的翻译
    '''
    conn, cur = get_conn_and_cursor()
    sql = r'''
        UPDATE strs
        SET jp = %s
        WHERE master_key = %s
        '''
    cur.execute(sql, (jp, key))
    conn.commit()


def import_all_imgs(f):
    '''
    导入图片数据
    '''
    print 'processing db', f
    conn = sqlite3.connect(f)
    c = conn.cursor()
    c.execute('SELECT id, master_key, img FROM img')
    row = c.fetchone()
    while row:
        (cid, master_key, img) = row
        img_path = 'img/' + str(cid) + '.png'
        with open(img_path, 'w') as f:
            f.write(img)
            insert_img((master_key, img_path))
        row = c.fetchone()


def import_master(db_path):
    '''
    导入master
    英文已经被解码，中文解码有问题
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, key, en_value, zh_value FROM master')
    row = c.fetchone()
    while row:
        (mid, key, en, zh) = row
        insert_str((key, urllib.unquote_plus(en), zh))
        row = c.fetchone()

    c.execute('SELECT id, master_key, translate_value FROM translation')
    row = c.fetchone()
    while row:
        (tid, key, jp) = row
        update_jp(key, jp)
        row = c.fetchone()
    conn.close()


if __name__ == '__main__':
    # db_path = 'db'
    # for f in os.listdir(db_path):
        # import_all_imgs(join(db_path, f))
    import_master('./master.db')
