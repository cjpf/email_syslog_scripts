#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will accept metadata for an email as sent from Barracuda
Email Security Service.

CJ Pfenninger
January 2020

Some more detailed description of this script goes here.
"""

import shelve
import json


def print_data(data):
    print(json.dumps(data, indent=2))


def store(data, key):
    _store_data(data.get('src_ip'), key, 'src_ip_shelf.db')
    _store_data(data.get('domain_id'), key, 'domain_id_shelf.db')
    _store_data(data.get('ptr_record'), key, 'ptr_record_shelf.db')
    _store_data(data.get('attachments'), key, 'attachments_shelf.db')
    _store_data(data.get('recipients'), key, 'recipients_shelf.db')
    _store_data(data.get('hdr_to'), key, 'hdr_to_shelf.db')
    _store_data(data.get('dst_domain'), key, 'dst_domain_shelf.db')
    _store_data(data.get('subject'), key, 'subject_shelf.db')
    _store_data(data.get('size'), key, 'size_shelf.db')
    _store_data(data.get('env_from'), key, 'env_from_shelf.db')
    _store_data(data.get('timestamp'), key, 'timestamp_shelf.db')
    print(key, 'stored.')
    return 0


def _store_data(data, key, db_name):
    db = shelve.open(db_name)
    db[key] = data
    db.close()
