#管理Cookie

import pickle
import pymysql
# from selenium import webdriver

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import SqlManager as Sql
# import selenium.webdriver.support.ui as ui
import requests
import time
from bs4 import BeautifulSoup

class CookieManager():
    def __init__(self,dbname,tname):
        self.dbname = dbname
        self.tablename = tname
        self.sqlman = Sql.sqlmanager()


    #将账号和密码转换成cookie,需要手动进行验证
    def get_cookie_from_web(self,weibo_account,weibo_password):
        url_login = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Flogin.weibo.cn%2Flogin%2F'
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = Chrome(options=option)
        # driver = webdriver.Chrome()
        driver.get(url_login)
        time.sleep(3)
        driver.find_element_by_xpath('//input[@type="text"]').send_keys(weibo_account) # 改成你的微博账号
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(weibo_password) # 改成你的微博密码
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="loginAction"]').click() # 点击登录
        # 获得 cookie信息
        time.sleep(5)
        cookie_list1 = driver.get_cookies()
        time.sleep(5)
        cookie_list2 = driver.get_cookies()
        time.sleep(5)
        cookie_list3 = driver.get_cookies()
        cookstring1 = ''
        for cook in cookie_list1:
            cookstring1 += cook['name']
            cookstring1 += '='
            cookstring1 += cook['value']
            cookstring1 += ';'
        cookstring2 = ''
        for cook in cookie_list2:
            cookstring2 += cook['name']
            cookstring2 += '='
            cookstring2 += cook['value']
            cookstring2 += ';'
        cookstring3 = ''
        for cook in cookie_list3:
            cookstring3 += cook['name']
            cookstring3 += '='
            cookstring3 += cook['value']
            cookstring3 += ';'
        cookstring_list = [cookstring1,cookstring2,cookstring3]
        return cookstring_list

    #检测cookie是否有效
    def check_cookie(self,cookstring):
        cook = {}
        cook["Cookie"] = cookstring
        url = 'https://weibo.cn/repost/H4jIguo7g'
        response = requests.get(url , cookies = cook)
        print(response.text)
        code = (response.status_code)
        while code > 200:  #
            print(code)
            time.sleep(3)
            response = requests.get(url, cookies=cook)
            code = response.status_code
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        p = soup.find('title').text
        print(p)
        if '新浪通行证' in p or '登录' in p or '请'in p:
            flag = 0
        else:
            flag = 1 # 真的是有效cookie
        return flag

    #更新已有的cookie
    def Updatecookie(self,cookie,username):
        self.sqlman.updatesql(self.dbname,self.tablename,'flag','100 where username = "'+ username +'"')
        self.sqlman.updatesql(self.dbname,self.tablename,'cookie',cookie + ' where username = "'+ username +'"')
        print("cookie插入成功")


    #从数据库中获取一条记录
    def getrecordfromsql(self):
        record  = self.sqlman.getsthfromsql(self.dbname,self.tablename,'cookie, username, password, flag',0,0,'where flag = 0')
        print(record)
        [cookie,username,password,flag] = record
        return cookie,username,password

    #更新所有的cookies
    def updateCookies(self):
        for i in range(10):
            cookie, username, password = self.getrecordfromsql()
            if not self.check_cookie(cookie): #cookie是否有效
                cookstring_list = self.get_cookie_from_web(username,password)
                print(cookstring_list)
                for cookstring in cookstring_list:
                    if self.check_cookie(cookstring) :
                        self.sqlman.updatesql(self.dbname,self.tablename,'cookie',cookstring + ' where username = ' + username)
                        self.sqlman.updatesql(self.dbname, self.tablename, 'flag', '100' + ' where username = ' + username)
                        self.Updatecookie(cookstring,username)
            else:
                self.setflag100(cookie)

    def getcookiefromsql(self):
        tablename = self.tablename
        conn = pymysql.connect(host="127.0.0.1",
                               port=3306,
                               user="root",
                               passwd='',
                               db= self.dbname,
                               charset='utf8'
                               )
        cursor = conn.cursor()  # 游标对象，用于执行查询和获取结果
        sql = 'select max(flag) from %s;' \
              % (pymysql.escape_string(tablename)
                 )
        cursor.execute(sql)
        maxflag = cursor.fetchone()
        maxflag = int(maxflag[0])
        print(maxflag)
        if maxflag > 0:
            sql = 'select * from %s where flag = %u;' \
                  % (pymysql.escape_string(tablename),
                     maxflag
                     )
            cursor.execute(sql)
            record = cursor.fetchone()
            cookie,username,password,flag = record
            # print(type(flag))
            new_flag = flag - 1
            sql = 'update %s set flag = %u where username = ("%s");' % (
                pymysql.escape_string(tablename), new_flag, pymysql.escape_string(username))
            cursor.execute(sql)
            conn.commit()
            return cookie
        else:
            self.updateCookies()
            self.getcookiefromsql()
        cursor.close()
        conn.close()
        # return cookie,username,password

    def setflag100(self,cookie):
        self.sqlman.updatesql(self.dbname,self.tablename,'flag','100' + ' where cookie = "'+ cookie + '"')
        print("flag更新成功")

if __name__ == '__main__':
    dbname = 'cookiemanage'
    cookietablename = 'cookiesmanager'
    c = CookieManager(dbname,cookietablename)
    # cookie = c.getcookiefromsql()
    # print(cookie)
    # 插入cookie
    for i in range(10):
        cookie,username,password = c.getrecordfromsql()

        print(cookie)
        print(c.check_cookie(cookie))
        if not c.check_cookie(cookie) :
            cookstring_list = c.get_cookie_from_web(username,password)
            print(cookstring_list)
            for cookstring in cookstring_list:
                if c.check_cookie(cookstring) :
                    record = [cookstring,username,password,1]
                    c.sqlman.updatesql(dbname,cookietablename,'cookie','"' + cookstring + '" where username = "'+ username + '"')
        else:
            c.setflag100(cookie)
