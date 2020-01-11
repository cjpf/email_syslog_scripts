# -*- coding: utf-8 -*-
import os
import sqlite3

"""
Database utilities for sqlite

CJ Pfenninger
January 2020

"""
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), '/tmp/example.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    """Establish and return a connection to the sqlite database"""
    connection = sqlite3.connect(db_path)
    return connection


def build_tables():
    """
    Creates the tables necessary for storing email metadata
    """
    conn = db_connect()
    cursor = conn.cursor()
    # Mail Table
    mail_sql = '''CREATE TABLE IF NOT EXISTS mail
                    (
                    message_id, domain_id, account_id,
                    src_ip, ptr_record, env_from,
                    hdr_from, hdr_to, dst_domain, size,
                    subject, timestamp
                    )'''
    try:
        cursor.execute(mail_sql)
        conn.close()
    except sqlite3.OperationalError as e:
        print('Error creating mail table', e)
        conn.close()
