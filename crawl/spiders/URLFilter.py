#!/usr/bin/env python
#coding=utf-8
###############################################
#                                             #
#               URL BloomFilter               #
#                                             #
###############################################

from pybloomfilter import BloomFilter
import MySQLConnection
import os

class URLBloomFilter:
    dbconn = None
    cur = None
    urlbf = None
    sql = None

    def initdb(self, host = 'localhost', user = 'xxxx', passwd = 'xxxx', db = 'beauty', port = 3306, charset = 'utf8'):
        self.dbconn = MySQLConnection.MySQLConn()
        self.dbconn.connect(m_host = host, m_user = user, m_passwd = passwd, m_db = db)
        self.cur = self.dbconn.cursor()

    def initfilter(self, filename = './url.filter'):
        if os.path.isfile(filename):
            self.urlbf = BloomFilter.open(filename)
        else:
            self.urlbf = BloomFilter(10000000, 0.001, filename)
    def initclear(self, tablename = 'adds'):
        self.cur.execute('truncate table ' + tablename)

    def initsql(self, m_sql):
        self.sql = m_sql

    def add(self, url):
        if not self.urlbf.add(url):
            self.cur.execute(self.sql, url)
            return True
        else:
            return False

    def close(self):
        self.dbconn.commit()
        self.dbconn.close()
