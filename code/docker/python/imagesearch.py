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

    def create_tables(self):
        self.con.execute("create table imlist(filename)")
        self.con.execute("create table imwords(imid, wordid, vocname)")
        self.con.execute("create table imhistogram(imid, histogram, vocname)")
        self.con.execute("create index im_idx on imlist(filename)")
        self.con.execute("create index wordid_idx on imwords(wordid)")
        self.con.execute("create index imid_idx on imwords(imid)")
        self.con.execute("create index imidhist_idx on imhistograms(imid)")
        self.db_commit()

    def add_to_index(self, imname, descr):
        """
        Input the image and feature and map the vocabuary into the database
        :param imname:
        :param descr:
        :return:
        """
        if self.is_indexed(imname): return
        print("indexing", imname)

        # Get the Image ID
        imid = self.get_id(imname)

        # Get the word
        imwords = self.voc.paroject(descr)
        nbr_words = imwords.shape[0]

        # Relation the image to the each words
        for i in range(nbr_words):
            word = imwords[i]
            self.con.execute("insert into imwords(imid, wordid, vocname) "
                             "values (?,?,?)", (imid, word, self.voc.name))
        self.con.execute("insert into imhistograms(imid, histogram, vocname)"
                         "values (?,?,?)", (imid, pickle.dumps(imwords), self.voc.name))

    def is_indexed(self, imname):
        """
        If the imnae has index, return the True
        :param imname:
        :return:
        """
        im = self.con.execute("select rowid from imlist where filename='%s'" % imname).fetchone()
        return im != None

    def get_id(self, imname):
        """
        Getting the element ID, if istsi nothing, add it
        :param imname:
        :return:
        """
        cur = self.con.execute(
            "select rowid from imlist where filename='%s'" % imname)
        res=cur.fetchone()
        if res == None:
            cur = self.con.execute(
                "insert into imlist(filename) values ('%s') " % imname
            )
            return cur.lastrowid
        else:
            return res[0]