import pymysql

class sqlmanager(object):
    def __init__(self):
        pass

    #返回符合条件的项目
    #sth 是需要查询的项目
    #sths_flag = 0 时返回一条记录，sths_flag = 1 时返回所有记录的list
    #plus_flag = 0 时不更新记录，plus_flag = 1 时更新记录flag
    #注意flag需要是int型
    def getsthfromsql(self, dbname, tablename, sth, sths_flag = 0, plus_flag = 0, condition = ''):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db= dbname,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'select %s from %s' % (pymysql.escape_string(sth), pymysql.escape_string(tablename))
        print(sql)
        sql = sql + ' '+ condition
        print(sql)
        cursor.execute(sql)
        if sths_flag : #返回所有
            result = cursor.fetchall()
            conn.commit()
            res = []
            for i in range(len(result)):
                # res.append(result[i])
                res.append(result[i][0])
            if plus_flag:
                sql2 = 'update %s set flag = flag + plusflag where %s = "%s"' % (pymysql.escape_string(tablename), pymysql.escape_string(sth), pymysql.escape_string(result))
                cursor.execute(sql2)
                conn.commit()
                conn.close()
            return res
        else:   #返回一条
            result = cursor.fetchone()
            result = list(result)
            if len(result)== 1:
                result = result[0]
            conn.commit()
            if plus_flag:
                sql2 = 'update %s set flag = flag + 1 where %s = "%s"' % (
                    pymysql.escape_string(tablename), pymysql.escape_string(sth), pymysql.escape_string(result))
                cursor.execute(sql2)
                conn.commit()
                conn.close()
            return result

    def create_table(self,db,tablename,columns):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db=db,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'CREATE TABLE ' + tablename + '('
        for c in columns:
            sql += c + ' varchar(255),'
        sql = sql[:-1]
        sql += ')'
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def Inserttosql_(self,db,tablename,record):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db=db,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'insert into ' + tablename + ' values ('
        for r in record:
            sql += '"' + str(r).replace('"',' ') + '"'
            sql += ','
        sql = sql[:-1] + ')'
        print(sql)
        cursor.execute(sql)
        conn.commit()
        print("记录插入成功！")
        conn.close()

    def Inserttosql(self,db,tablename,records):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db=db,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        for record in records:
            sql = 'insert into ' + tablename + ' values ('
            for r in record:
                sql += '"' + str(r).replace('"',' ') + '"'
                sql += r
                sql += ','
            sql = sql[:-1] + ')'
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print("记录插入成功！")
        conn.close()

    def updatesql(self,db,tablename,setwho,newvalue=''):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db=db,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'update ' + tablename + ' set ' + setwho + ' = ' +  str(newvalue)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def deletesql(self,db,tablename,condition = ''):
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db=db,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'delete from ' + tablename + ' ' + condition
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

#测试代码
s = sqlmanager()
# res = s.getsthfromsql('twitter','test','name',condition = 'where flag > 0', plus_flag=1)
# print(res)
# res1 = s.updatesql('twitter','test','flag','flag+1','where name = "法制晚报"')
# res2 = s.deletesql('twitter','test','where name = "法制晚报"')
# rec = ['111','11',0]
# res3 = s.Inserttosql('twitter','test',rec)
