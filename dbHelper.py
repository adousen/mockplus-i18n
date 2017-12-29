#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser

import MySQLdb as mdb

config = ConfigParser()
config.read('config.ini')


def get_db_config(option):
    try:
        return config.get('mysql', option)
    except:
        return ""


def get_db_conn():
    """get a db connection"""
    conn = mdb.connect(host=get_db_config("host"),
                       user=get_db_config("user"),
                       passwd=get_db_config("passwd"),
                       db=get_db_config("db"))
    conn.set_character_set('utf8')
    return conn


def get_cursor(conn):
    """
    获取 cursor
    :param conn: 数据库连接
    :return: cursor
    """
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET UTF8;')
    cursor.execute('SET character_set_connection=utf8;')
    return cursor


def get_conn_and_cursor():
    conn = get_db_conn()
    cursor = get_cursor(conn)
    return conn, cursor
