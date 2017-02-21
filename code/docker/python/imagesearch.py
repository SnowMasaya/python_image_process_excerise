# -*- coding:utf-8 -*-
# !/usr/bin/python3

import pickle
from sqlite3 import dbapi2 as sqlite
from functools import cmp_to_key
from math import sqrt
from numpy import *
from PIL import Image
from matplotlib.pyplot import imshow
from pylab import *


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
        self.con.execute("create table imhistograms(imid, histogram, vocname)")
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
        imwords = self.voc.project(descr)
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


class Searcher(object):
    """
    Data Base Searcher
    """
    def __init__(self, db, voc):
        """
        Initialize database name and vocabuary
        :param db:
        :param voc:
        """
        self.con = sqlite.connect(db)
        self.voc = voc

    def __del__(self):
        self.con.close()

    def candidates_from_word(self, imword):
        """
        Get the image list include by the imword
        :param imword:
        :return:
        """
        im_ids = self.con.execute(
            "select distinct imid from imwords where wordid=%d" % imword
        ).fetchall()
        return [i[0] for i in im_ids]

    def candidates_from_histogram(self, imwords):
        """
        Get the multi simillaier word image list
        :param imwords:
        :return:
        """
        words = imwords.nonzeros()[0]

        candidates = []
        for word in words:
            c = self.candidates_from_word(word)
            candidates += c

        tmp = [(w, candidates.count(w)) for w in set(candidates)]
        tmp.sort(cmp=lambda x,y:cmp(x[1], y[1]))
        tmp.reverse()

        return [w[0] for w in tmp]

    def candidates_from_word(self, imword):
        """
        Get the Image list include in the imword
        :param imword:
        :return:
        """
        im_ids = self.con.execute("select distinct imid from imwords where wordid=%d "
                                  % imword).fetchall()
        return [i[0] for i in im_ids]

    def candidates_from_histogram(self, imwords):
        """
        Get the image list include in the multiple similiar words
        :param imwords:
        :return:
        """
        words = imwords.nonzero()[0]

        candidates = []
        for word in words:
            c = self.candidates_from_word(word)
            candidates += c

        tmp = [(w, candidates.count(w)) for w in set(candidates)]
        sorted(tmp, key=cmp_to_key(cmp))
        tmp.reverse()

        return [w[0] for w in tmp]

    def get_imhistogram(self, imname):
        """
        Return the word histogram
        :param imname:
        :return:
        """
        im_id = self.con.execute(
            "select rowid from imlist where filename='%s'" % imname).fetchone()
        if im_id is not None:
            s = self.con.execute(
                "select histogram from imhistograms where rowid='%d'" % im_id
            ).fetchone()
            return pickle.loads(s[0])

    def query(self, imname):
        """
        Get the Imname image list
        :param imname:
        :return:
        """
        h = self.get_imhistogram(imname=imname)
        if h is not None:
            candidates = self.candidates_from_histogram(h)

            matchscores = []
            for imid in candidates:
                cand_name = self.con.execute(
                    "select filename from imlist where rowid=%d" % imid
                ).fetchone()
                cand_h = self.get_imhistogram(cand_name)
                cand_dist = sqrt(sum((h - cand_h)**2))
                matchscores.append((cand_dist, imid))

            matchscores.sort()
            return matchscores

    def get_filename(self, imid):
        """
        Return the file name relationship with the image id
        :param imid:
        :return:
        """
        s = self.con.execute(
            "select filename from imlist where rowid='%d'" % imid
        ).fetchone()
        return s[0]

def compute_ukbench_score(src, imlist):
    """
    Return the best fourth and the correct average score
    :param imlist:
    :return:
    """
    nbr_images = len(imlist)
    pos = zeros((nbr_images, 4))
    for i in range(nbr_images):
        query_data = src.query(imlist[i])
        if query_data is not None:
            for w in query_data[:4]:
                pos[i] = [w[1] - 1]

    score = array([ (pos[i]//4)==(i//4) for i in range(nbr_images)]) * 1.0
    return sum(score) / (nbr_images)

def plot_results(src, res):
    """
    Show the search result image
    :param src:
    :param res:
    :return:
    """
    figure()
    nbr_results = len(res)
    for i in range(nbr_results):
        imname = src.get_filename(res[i])
        subplot(1, nbr_results, i + 1)
        imshow(array(Image.open(imname.strip())))
        axis("off")
    show()

def cmp(a, b):
    if a == b:
        return 0
    if a < b:
        return -1
    else:
        return 1