#!/usr/bin/env python
#coding=utf-8

import GaAddItem

if __name__ == '__main__':
    obj = GaAddItem.GaAddItem()
    obj.initpath()
    obj.initdb()
    obj.add()
    obj.close()
    print 'done'
