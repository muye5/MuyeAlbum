#!/usr/bin/env python
#coding=utf-8
###############################################
#                                             #
#               MySQL By Python               #
#                                             #
###############################################

import MySQLdb
import sys

class MySQLConn:
    conn = None

    def connect(self, m_host, m_user, m_passwd, m_db, m_port = 3306, m_charset = 'utf8'):
        self.conn = MySQLdb.connect(host = m_host, user = m_user, passwd = m_passwd, db = m_db, port = m_port, charset = m_charset)
        print "connect successfully"

    def cursor(self):
        try:
            return self.conn.cursor()
        except (AttributeError, MySQLdb.OperationalError):
            print "except in cursor() and will exit"
            self.close()
            sys.exit(1)

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()
