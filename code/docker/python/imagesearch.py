# -*- coding:utf-8 -*-
# !/usr/bin/python3

import pickle
from sqlite3 import dbpi2 as sqlite

class Indexer(object):
    """
    Search the Image data
    """
    def __init__(self, db, voc):
        """
        # Args
        :param db: setting database name
        :param voc: setting vocabuary object
        """
        self.con = sqlite.connect(db)
        self.voc = voc

    def __del__(self):
        self.con.close()

    def db_commit(self):
        self.con.commit()
