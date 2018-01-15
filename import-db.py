# -*- coding: utf-8 -*-
import sqlite3
from dbHelper import get_conn_and_cursor
import urllib

IS_DEV = True

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
        img_path = ''
        http_path = ''
        if IS_DEV:
            img_path = 'img/' + str(cid) + '.png'
            http_path = 'http://192.168.2.88:9922/img/' + str(cid) + '.png'
        else:
            img_path = '/srv/file/i18n/img/' + str(cid) + '.png'
            http_path = 'https://file.mockplus.com/i18n/img/' + str(cid) + '.png'
        with open(img_path, 'w') as f:
            f.write(img)
            insert_img((master_key, http_path))
        row = c.fetchone()


def decode_text(txt):
    return urllib.unquote_plus(txt).encode('latin-1').decode('utf-8')


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
        insert_str((key, decode_text(en), decode_text(zh)))
        row = c.fetchone()

    c.execute('SELECT id, master_key, translate_value FROM translation')
    row = c.fetchone()
    while row:
        (tid, key, jp) = row
        update_jp(key, decode_text(jp))
        row = c.fetchone()
    conn.close()


def import_review(db_path, uid):
    '''
    导入校对信息
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT master_key, proof, remark FROM translation')
    row = c.fetchone()
    while row:
        (mid, proff, remark) = row
        insert_review(uid, (mid, decode_text(proff), decode_text(remark)))
        row = c.fetchone()


def insert_review(uid, data):
    '''
    插入 review
    '''
    conn, cur = get_conn_and_cursor()
    sql = '''
    INSERT INTO `review` (
        `master_key`, `review`, `remark`, `uid`, `addtime`, `state`
    )
    VALUES (
        %s, %s, %s, %s, now(), 0
    )
    '''
    (mid, proff, remark) = data
    cur.execute(sql, (mid, proff, remark, uid))
    conn.commit()


def prepare():
    conn, cur = get_conn_and_cursor()
    sqls = [
        'DROP TABLE IF EXISTS `strs`;',
        'DROP TABLE IF EXISTS `img`;',
        'DROP TABLE IF EXISTS `review`',
        r'''
        CREATE TABLE `strs` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `master_key` varchar(300) NOT NULL,
            `en` text NOT NULL,
            `cn` text NOT NULL,
            `jp` text NOT NULL,
            `addtime` datetime NOT NULL,
            `state` tinyint(4) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE = InnoDB DEFAULT CHARSET=utf8
        ''',
        r'''
        CREATE TABLE `img` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `master_key` varchar(300) NOT NULL,
            `img` varchar(100) NOT NULL,
            `addtime` datetime NOT NULL,
            `state` tinyint(4) NOT NULL DEFAULT '0',
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8''',
        r'''
        CREATE TABLE `review` (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            `master_key` VARCHAR(300) NOT NULL,
            `review` TEXT NOT NULL,
            `remark` TEXT NOT NULL,
            `uid` INT NOT NULL,
            `addtime` DATETIME NOT NULL,
            `state` INT NOT NULL
        ) ENGINE = INNODB DEFAULT CHARSET = utf8;
        '''
    ]
    for sql in sqls:
        cur.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    prepare()
    db_path = './master.db'
    import_master(db_path)
    import_all_imgs(db_path)
    import_review(db_path, 1)
