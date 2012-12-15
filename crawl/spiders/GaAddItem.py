#!/usr/bin/env python
#coding=utf-8
# galleryremote: /usr/share/pyshared/galleryremote/gallery.py

from galleryremote import Gallery
import MySQLConnection
import hashlib
import datetime
import sys
import os

class GaAddItem:
    path = None
    conn = None
    cur = None
    gal = None
    log = None

    def initpath(self, pa = '/directory of images/'):
        self.path = pa
        self.log = open('./log/log.' + str(datetime.date.today()), 'a')
        print >> self.log, '=============================  ', datetime.date.today(), '  ============================'

    def initdb(self, host = 'localhost', user = 'xxxx', passwd = 'xxxx', db = 'beauty', port = 3306, charset = 'utf8'):
        self.conn = MySQLConnection.MySQLConn()
        self.conn.connect(m_host = host, m_user = user, m_passwd = passwd, m_db = db)
        self.cur = self.conn.cursor()
        self.gal = Gallery('http://localhost/gallery2', 2)
        self.gal.login('xxxx','xxxx')

    def add(self):
        album = self.gal.fetch_albums()['7']
        self.cur.execute("""select url from adds""");
        results = self.cur.fetchall()
        items = []
        today = str(datetime.date.today())
        cnt = 0
        for url in results:
            hs = hashlib.sha1()
            hs.update(url[0])
            imagename = self.path + hs.hexdigest() + '.jpg'
            if os.path.isfile(imagename):
                cnt = cnt + 1
                self.gal.add_item(album['name'], imagename, today+'-'+str(cnt), 'show_'+str(cnt))
                items.append(url[0])
            else:
                print >> self.log, imagename, ' not founded!'
        self.cur.executemany('insert into url (url) values (%s)', items)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
        self.log.close()

