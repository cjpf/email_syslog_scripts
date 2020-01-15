# -*- coding: utf-8 -*-
import os
import sqlite3

"""
Database utilities for sqlite

CJ Pfenninger
January 2020

"""
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), '/tmp/essmail.sqlite3')


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
    # Messages Table
    messages_sql = '''CREATE TABLE IF NOT EXISTS messages
                    (
                    message_id, account_id, domain_id, src_ip,
                    ptr_record, env_from, hdr_from, hdr_to,
                    dst_domain, size, subject, timestamp
                    )'''
    # Recipients Table
    recipients_sql = '''CREATE TABLE IF NOT EXISTS recipients
                    (
                    message_id, action, reason, reason_extra,
                    delivered, delivery_detail, email
                    )'''
    # Attachments Table
    attachments_sql = '''CREATE TABLE IF NOT EXISTS attachments
                    (
                    message_id, name
                    )'''

    try:
        cursor.execute(messages_sql)
        cursor.execute(recipients_sql)
        cursor.execute(attachments_sql)
        conn.close()
    except sqlite3.OperationalError as e:
        print('Error creating tables: ', e)
        conn.close()
