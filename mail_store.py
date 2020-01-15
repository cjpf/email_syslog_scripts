#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
mail_store manages the database interactions for mail_parser

CJ Pfenninger
January 2020

"""

import db_utils
import sqlite3


def build_store():
    """
    calls the build_tables utility
    tables are only created if they do not yet exist
    """
    db_utils.build_tables()


def store(data):
    """stores metadata for a single message"""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    row_ids = {}
    try:
        _store(cursor, 'messages', (
            data.get('message_id'),
            data.get('account_id'),
            data.get('domain_id'),
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
    """stores an object"""
    insert_string = 'INSERT INTO ', table, ' VALUES (', _param_string(
        len(t)), ')'
    try:
        cur.execute(''.join(insert_string), t)
        return cur.lastrowid
    except sqlite3.OperationalError as e:
        return e


def _store_list(cur, table, message_id, t):
    """stores a list objects"""
    if t is None:
        insert_string = 'INSERT INTO ', table, ' VALUES (?, ?)'
        try:
            cur.execute(''.join(insert_string), (message_id, 'NULL'))
            return cur.lastrowid
        except sqlite3.OperationalError as e:
            return e

    for row in t:
        insert_string = 'INSERT INTO ', table, ' VALUES (', _param_string(
            len(row)+1), ')'
        data = _convert_data(message_id, row)
        try:
            cur.execute(''.join(insert_string), data)
        except sqlite3.OperationalError as e:
            print(e)
            return -1
    return 0


def _convert_data(id, row):
    """re-organizes the data for storage"""
    data = [id]
    for x in row:
        data.append(row[x])
    return data


def _param_string(t):
    """builds query parameters string"""
    params = ''
    for x in range(t):
        params += '?,'
    return params.rsplit(',', 1)[0]
