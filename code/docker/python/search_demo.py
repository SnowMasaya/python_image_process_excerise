# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import cherrypy, os, urllib, picklefrom numpy import *
import imagesearch


class SearchDemo:

    def __init__(self):
        f = open("webimlist.txt")
        self.imlist = f.readlines()
        f.close()
        self.nbr_images = len(self.imlist)
