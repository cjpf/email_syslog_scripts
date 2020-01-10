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


def print_data(data):
    """."""
    print(json.dumps(data, indent=2))


def build_store():
    db_utils.build_tables()


def store(data):
    """."""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    t = (
        data.get('message_id'),
        data.get('src_ip'),
        data.get('ptr_record'),
        data.get('env_from'),
        data.get('hdr_from'),
        data.get('hdr_to'),
        data.get('size'),
        data.get('subject'),
        data.get('timestamp')
    )
    cursor.execute('INSERT INTO mail VALUES (?,?,?,?,?,?,?,?,?)', t)
    conn.commit()
    conn.close()
    return


def read_all():
    """."""
    conn = db_utils.db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mail')
    data = cursor.fetchall()
    conn.close()
    return data
