# -*- coding: utf-8 -*-
import os
import sqlite3

"""
Database utilities for sqlite

CJ Pfenninger
January 2020

"""
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'example.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    """Establish and return a connection to the sqlite database"""
    connection = sqlite3.connect(db_path)
    return connection


def build_tables():
    """
    Checks to see if the tables exist and creates them if needed
    """
    conn = db_connect()
    cursor = conn.cursor()
    # Mail Table
    mail_sql = '''CREATE TABLE mail
                    (message_id, src_ip, ptr_record, env_from,
                    hdr_from, hdr_to, size, subject, timestamp)'''
    try:
        print('Creating mail table')
        cursor.execute(mail_sql)
        print('mail table created')
    except sqlite3.OperationalError:
        print('mail table exists')
        conn.close()
