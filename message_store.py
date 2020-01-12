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
    t = (
        data.get('message_id'),
        data.get('domain_id'),
        data.get('account_id'),
        data.get('src_ip'),
        data.get('ptr_record'),
        data.get('env_from'),
        data.get('hdr_from'),
        data.get('hdr_to'),
        data.get('dst_domain'),
        data.get('size'),
        data.get('subject'),
        data.get('timestamp'),
    )

    try:
        cursor.execute(
            'INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', t)
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except sqlite3.OperationalError:
        conn.rollback()
        conn.close()
        return -1


# def _store_message(data):


def _store_list(cur, table, message_id, t):


# def _store_domain(data):



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
