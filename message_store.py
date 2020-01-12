#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will accept metadata for an email as sent from Barracuda
Email Security Service.

CJ Pfenninger
January 2020

Some more detailed description of this script goes here.
"""

import json
import db_utils
import sqlite3


def print_data(data):
    """."""
    print(json.dumps(data, indent=2))


def build_store():
    """."""
    db_utils.build_tables()


def store(data):
    """Stores metadata for a single message"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    row_ids = {}
    try:
        _store(cursor, 'messages', (
            data.get('message_id'),
            data.get('src_ip'),
            data.get('ptr_record'),
            data.get('env_from'),
            data.get('hdr_from'),
            data.get('hdr_to'),
            data.get('dst_domain'),
            data.get('size'),
            data.get('subject'),
            data.get('timestamp'),
        ))
        row_ids['message_row_id'] = cursor.lastrowid

        _store(cursor, 'accounts', (
            data.get('message_id'),
            data.get('account_id')
        ))
        row_ids['accounts_row_id'] = cursor.lastrowid

        _store(cursor, 'domains', (
            data.get('message_id'),
            data.get('domain_id')
        ))
        row_ids['domains_row_id'] = cursor.lastrowid

        _store_list(cursor, 'recipients', data.get('message_id'), (
            data.get('recipients')
        ))
        row_ids['recipients_row_id'] = cursor.lastrowid

        _store_list(cursor, 'attachments', data.get('message_id'), (
            data.get('attachments')
        ))
        row_ids['attachments_row_id'] = cursor.lastrowid

        conn.commit()
        conn.close()
        return row_ids
    except sqlite3.OperationalError:
        conn.rollback()
        conn.close()
        return -1


def _store(cur, table, t):
    """Stores tupled data into a single table"""
    insert_string = 'INSERT INTO ', table, ' VALUES (', _param_string(len(t)), ')'
    try:
        cur.execute(''.join(insert_string), t)
        return cur.lastrowid
    except sqlite3.OperationalError as e:
        return e


def _store_list(cur, table, message_id, t):
    """Stores a list of rows into a single table"""
    if t is None:
        insert_string = 'INSERT INTO ', table, ' VALUES (?, ?)'
        try:
            cur.execute(''.join(insert_string), (message_id, 'NULL'))
            return cur.lastrowid
        except sqlite3.OperationalError as e:
            return e

    for row in t:
        insert_string = 'INSERT INTO ', table, ' VALUES (', _param_string(len(row)+1), ')'
        data = _convert_data(message_id, row)
        try:
            cur.execute(''.join(insert_string), data)
        except sqlite3.OperationalError as e:
            print(e)
            return -1
    return 0


def _convert_data(id, row):
    data = [id]
    for x in row:
        data.append(row[x])
    return data


def _param_string(t):
    """
    Builds the string for query parameters
    Accepts an integer
    """
    params = ''
    for x in range(t):
        params += '?,'
    return params.rsplit(',', 1)[0]


def read_messages():
    """Returns all message rows"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    data = cursor.fetchall()
    conn.close()
    return data


def read_accounts():
    """Returns all account rows"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    data = cursor.fetchall()
    conn.close()
    return data


def read_domains():
    """Returns all domain rows"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM domains')
    data = cursor.fetchall()
    conn.close()
    return data


def read_recipients():
    """Returns all recipient rows"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipients')
    data = cursor.fetchall()
    conn.close()
    return data


def read_attachments():
    """Returns all attachment rows"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attachments')
    data = cursor.fetchall()
    conn.close()
    return data
