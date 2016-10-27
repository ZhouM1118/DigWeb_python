# -*- coding: UTF-8 -*-
import sys
# print(sys.path)
# #import __init__
# sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb/dao')
# print(sys.path)
from db import dbConnector

def insert(tableClass, params):
    # 单例模式
    connector = dbConnector.dbConnector
    db = connector.getDB('intelligentler')

    sql = 'insert into ' + str(tableClass.__name__).lower() + '('
    kstr = ''
    vstr = ''
    for (k,v) in params.items():
        if '__' in k:
            kreu = k.split('__')[1]
        else:
            kreu = k
        kstr += str(kreu) + ', '
        if isinstance(v, str):
            vstr += "'" + v + "', "
        else:
            vstr += str(v) + ', '
    sql += kstr[:len(kstr)-2] + ') values (' + vstr[:len(vstr)-2] + ')'
    print('insert sql is ' + sql)

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('insert sql except happened!')
        db.rollback()
    result = cursor.rowcount
    db.close()
    # result = 1
    return result

def delete(tableClass, params):
    print('=====delete=====')
    # 单例模式
    connector = dbConnector.dbConnector
    db = connector.getDB('intelligentler')

    sql = 'delete from ' + str(tableClass.__name__).lower() + ' where '
    whereStr = ''
    for (k,v) in params.items():
        whereStr += k + '=' + (("'" + v + "' and ") if isinstance(v, str) else (str(v) + ' and '))
    # print('whereStr is ' + whereStr)
    sql += whereStr[:len(whereStr) - 5]
    # print('delete sql is ' + sql)

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('delete sql except happened!')
        db.rollback()
    result = cursor.rowcount
    db.close()
    return result

def update(tableClass, set_params, where_params):
    print('=====update=====')
    # 单例模式
    connector = dbConnector.dbConnector
    db = connector.getDB('intelligentler')

    sql = 'update ' + str(tableClass.__name__).lower() + ' set '
    setStr = ''
    whereStr = ''
    for (k,v) in set_params.items():
        setStr += k + '=' + (("'" + v + "', ") if isinstance(v, str) else (str(v) + ', '))
    print('setStr is ' + setStr)
    for (k1,v1) in where_params.items():
        whereStr += k1 + '=' + (("'" + v1 + "' and ") if isinstance(v1, str) else (str(v1) + ' and '))
    print('whereStr is ' + whereStr)
    sql += setStr[:len(setStr) - 2] + ' where ' + whereStr[:len(whereStr) - 5]
    print('update sql is ' + sql)

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('update sql except happened!')
        db.rollback()
    result = cursor.rowcount
    db.close()
    return result

def findFirstByParams(tableClass, params):
    # 单例模式
    connector = dbConnector.dbConnector
    db = connector.getDB('intelligentler')

    sql = 'select * from ' + str(tableClass.__name__).lower() + ' where '
    kStr = ''
    vStr = ''
    for (k, v) in params.items():
        kStr += str(k.split('__')[1] if '__' in k else k) + ', '
        vStr += ("'" + v + "', ") if isinstance(v, str) else (str(v) + ', ')
    sql += kStr[:len(kStr) - 2] + '=' + vStr[:len(vStr) - 2]
    print('find sql is ' + sql)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('find sql except happened!')
        db.rollback()
    all = cursor.fetchall()
    db.close()
    table = tableClass.gene(tableClass, all[0][1:len(all[0])])
    return table

def test(tableClass, params):
    sql = ''
    for (k,v) in params.items():
        sql += v
    print('sql is ' + sql)
    # show_version = do(db, sql)
    # print('Database version : %s ' % show_version)
# db = connector.getDB('intelligentler')
# show_version = do(db, 'select version()')
# print('Database version : %s ' % show_version)
if __name__ == '__main__':
    k = 123
    result = k+' is str' if isinstance(k, str) else str(k) + ' is not str'
    print(result)