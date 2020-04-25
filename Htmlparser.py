# -*- coding: utf-8 -*-
import codecs
import random
import time

import pymysql
import requests
from bs4 import BeautifulSoup
import re
import CookieManager as CookManager
import IpManager as Ip
import random

# ***********基本信息请谨慎更改***********************************************************************************************
page = 'https://weibo.cn'  # 简易版微博首页地址
main_page = 'https://weibo.com'  # 正式版微博首页地址
comment_page = 'https://weibo.cn/repost/'  # 简易版微博评论页面地址
##请登录帐号查找自己的cookie填入此处
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"}
# ***************************************************************************************************************************


class html_parser():

    def __init__(self):
        # 每个记录提取来一遍
        # self.bf = Bl.BloomCheckFunction()  # 对象初始化 只需要初始化一遍
        self.dbname = 'cookiemanage'
        self.tname = 'cookiesmanager'
        self.c = CookManager.CookieManager(self.dbname,self.tname)
        #从数据库中获取cook
        self.p = Ip.IpManager()
        self.cooklist = self.getcookfromsql()
        self.proxy = self.p.getproxyfromipsql(10)
        self.pro = ''

    # 弄好的list 中随机取一个cook
    def getcook(self):
        cookielist = self.cooklist
        i = random.randrange(len(cookielist))
        cook = cookielist[i]
        cookie = {}
        cookie["Cookie"] = cook
        print(cookie)
        return cookie

    #从数据库中取出一些cook 组成list
    def getcookfromsql(self):
        cooklist = []
        for i in range(10):
            cook = self.c.getcookiefromsql()
            cooklist.append(cook)
        print(cooklist)
        return cooklist

    def getnormalresponceofurl(self,url):
        response = requests.get(url,  headers=headers, cookies = self.getcook() ,timeout=3)
        return response

    def getresponceofotherurl(self,url):
        response = requests.get(url,  headers = headers ,timeout=2)
        return response

    #从一个微博url中获取内容 + 奖惩对应的proxy 和 cookie
    def getresponceofurl(self, url, keyword = ''):
        pp = Ip.IpManager()
        if self.pro == '':
            self.pro = pp.getproxyfromipsql(1)[0]
            # print(self.pro)
        flag = 1
        response = ''
        while True:
            try:
                # print(self.pro)
                # response = requests.get(url, cookies = self.getcook(), headers = headers, proxies = self.pro, timeout = 5 ,verify=False )
                t = random.randrange(0, 8)
                if t == 4:
                    response = requests.get(url, cookies = self.getcook(), headers = headers, timeout = 5 )
                else:
                    response = requests.get(url, cookies = self.getcook(), headers = headers, proxies = self.pro, timeout = 5 )
                # print(response)
                code = response.status_code
                if not code > 200 :
                    # print(response.text)
                    if  keyword in response.text:
                        pp.rewardthisproxy(self.pro)
                        return response
                else:
                    pp.punishthisproxy(self.pro)
                    self.pro = pp.getproxyfromipsql()[0]
                    flag += 1
                    if flag > 100:
                        return response
            except Exception as e:
                print(str(e))
                pp.punishthisproxy(self.pro)
                self.pro = pp.getproxyfromipsql()[0]
                flag += 1
                if flag > 10:
                    return response
            # pp.deletethisproxy(self.pro)
            # pp.punishthisproxy(self.pro)

    def getcitybyurl(self, url):  # 对每个链接都返回一页record
        print(url)
        records = []
        t = random.randrange(0, 2)
        t = float(float(t) / 5)
        print(t)
        time.sleep(t)
        try:
            response = self.getresponceofurl(url)
            html = response.content
            print(html)
            # newurl = (str(html)).split(';')[2]
            # print(newurl)
            # response = self.getnormalresponceofurl(newurl)
            # html = response.content

            soup = BeautifulSoup(html, "html.parser")
            # r 算是所有的帖子节点
            r = soup.find('span', attrs={"class": "ctips"})
            print(r)
            return r.text
        except:
            return None

    def geturlsbyurl(self,url):
        print(url)
        records = []
        t = random.randrange(0, 2)
        t = float(float(t) / 5)
        print(t)
        time.sleep(t)
        try:
            response = self.getresponceofurl(url)
            html = response.content
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            try:
                r = soup.find('span', attrs={"class": "ctips"})
                print(r.text)
            except:
                pass
            page = soup.find('span', attrs={"class": "list"}).text.split('第')[-1].split('页')[0]
            print(page)
            return page
        except:
            return None

    def gettweetbyurl(self, url):
        print(url)
        records = []
        t = random.randrange(0, 2)
        t = float(float(t) / 5)
        print(t)
        time.sleep(t)
        try:
            response = self.getresponceofurl(url)
            html = response.content
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            # r 算是所有的帖子节点
            rs = soup.findAll('div', attrs={"class": "content"})
            records = []
            for r in rs:
                content = r.find('p', attrs={"node-type": "feed_list_content"}).text.strip()
                print(content)
                name = r.find('a', attrs={"class": "name"}).text.strip()
                print(name)
                tim = r.find('p', attrs={"class": "from"}).find('a')
                tim_text = tim.text.strip()
                tim_link = tim.get('href')
                print(tim_text)
                print(tim_link)
                records.append([url,name,content,tim_text,tim_link])
            return records
        except:
            return None




    def getVolumebyurl(self, url):  # 对每个链接都返回一页record
        records = []
        t = random.randrange(0, 2)
        t = float(float(t) / 5)
        print(t)
        time.sleep(t)
        try:
            response = self.getresponceofurl(url)
            print(response)
            if (type(response)) == str:
                return ['-1','-1','-1']
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            print(soup)
            # r 算是所有的帖子节点
            r = soup.findAll('div', attrs={"class": "pms"})
            print(r)
            if r:
                return ['100','100','100']
            else:
                return ['-1','-1','-1']
        except Exception as e:
            print("页面解析失败，没有爬到新纪录")
            raise Exception()
        return records




if __name__ == '__main__':
    h = html_parser()
    #获取整个网页的内容
    # content = h.getresponceofurl('https://weibo.cn/comment/GEuPYfBtq')
    # print(content.text)
    # #获取整个网页中url的列表
    # list = h.getUrlList('GEuPYfBtq', 'comment')
    # print(list)
    # like = h.getLikebyurl('https://weibo.cn/attitude/GF3rA8loE')
    # print(like)
    comment = h.getCommentbyurl('https://weibo.cn/comment/GcMuFjaHU')
    print(comment)
    # repost = h.getRepostbyurl('https://weibo.cn/repost/GcMuFjaHU')
    # print(repost)


