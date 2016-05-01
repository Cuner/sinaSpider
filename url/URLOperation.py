#coding=utf-8
import MySQLdb
import hashlib
import time

def StoreURL(url,type):
    hash_md5 = hashlib.md5(url).hexdigest()

    db = MySQLdb.connect("localhost", "root", "123123", "sinaSpider")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = "INSERT INTO URLQueue (url,grabTime,is_grab,linkType,md5_1,md5_2,md5_3,md5_4,md5_5,md5_6,md5_7,md5_8," \
          "md5_9,md5_10,md5_11,md5_12,md5_13,md5_14,md5_15,md5_16,md5_17,md5_18,md5_19,md5_20,md5_21,md5_22," \
          "md5_23,md5_24,md5_25,md5_26,md5_27,md5_28,md5_29,md5_30,md5_31,md5_32) VALUES " \
          "('%s','%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
          "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %\
          (url,0,0,type,hash_md5[0],hash_md5[1],hash_md5[2],hash_md5[3],hash_md5[4],hash_md5[5],hash_md5[6],
           hash_md5[7],hash_md5[8],hash_md5[9],hash_md5[10],hash_md5[11],hash_md5[12],hash_md5[13],hash_md5[14],
           hash_md5[15],hash_md5[16],hash_md5[17],hash_md5[18],hash_md5[19],hash_md5[20],hash_md5[21],hash_md5[22],
           hash_md5[23],hash_md5[24],hash_md5[25],hash_md5[26],hash_md5[27],hash_md5[28],hash_md5[29],hash_md5[30],hash_md5[31])

    print sql
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print 'insert success'
    except:
        # Rollback in case there is any error
        db.rollback()
        print "insert fail"

    db.close()

def SelectURL(type):
    db = MySQLdb.connect("localhost", "root", "123123", "sinaSpider")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT * FROM URLQueue WHERE linkType='%d' AND is_grab = 0 LIMIT %d" % (type, 1)

    print sql
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0]
    except:
        # Rollback in case there is any error
        db.rollback()
        print "fail to select url"
        return False

    db.close()

def UpdateURL(id):
    db = MySQLdb.connect("localhost", "root", "123123", "sinaSpider")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "UPDATE URLQueue set grabTime='%d', is_grab=1 WHERE id = '%d'" % (time.time(),id)

    print sql
    try:
        # 执行sql语句
        cursor.execute(sql)
        db.commit()
        print 'update success'
    except:
        # Rollback in case there is any error
        db.rollback()
        print "fail to update url"

    db.close()