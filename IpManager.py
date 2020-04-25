#管理IP，构建和维护自己的IP代理池，防止电脑的IP被封号

import pickle
import pymysql
import SqlManager as Sql
import requests
import time
from bs4 import BeautifulSoup
import random
import json
import Htmlparser as parser
import re
import telnetlib



class IpManager():

    def __init__(self):
        self.tablename = 'newipmanager'
        self.sqlman = Sql.sqlmanager()
        self.db = 'twitter'

    #从数据库中选出所有可能有效的ip地址
    def getipfromsql(self):
        ip = self.sqlman.getsthfromsql(self.db,self.tablename,'ip',sths_flag = 1,condition = 'where flag > 0')
        return ip

    #转化成可以用的方式
    def todict(self,iplist):
        proxylist = []
        for newip in iplist :
            proxy = {}
            proxy['http'] = newip
            proxy['https'] = newip
            proxylist.append(proxy)
        return  proxylist

    #对于可行的proxy进行奖励
    def rewardthisproxy(self,proxy):
        if type(proxy) == dict:
            pro = proxy['http']
        else:
            pro = proxy
        print(pro)
        self.sqlman.updatesql(self.db,self.tablename,'flag', 'flag + 1 where ip = "'+ pro + '"')

    #对于不可行的proxy进行惩罚
    def punishthisproxy(self,proxy):
        if type(proxy) == dict:
            pro = proxy['http']
        else:
            pro = proxy
        print(pro)
        self.sqlman.updatesql(self.db, self.tablename, 'flag', 'flag - 1 where ip = "' + pro + '"')

    #删除proxy
    def deletethisproxy(self,proxy):
        if type(proxy) == dict:
            pro = proxy['http']
        else:
            pro = proxy
        print(pro)
        self.sqlman.deletesql(self.db, self.tablename, 'where ip = "' + pro + '"')

    #从获取到的所有可用ip中选出这么多个ip
    def getproxyfromipsql(self, numbers = 3):
        ip = self.getipfromsql()
        iplist = []
        for i in range(numbers):
            newip = random.choices(ip)[0]
            iplist.append(newip)
        # print(iplist)
        proxy = self.todict(iplist)
        # print(proxy)
        # print(proxy)
        return proxy

    def checkip(self, ip):
        try:
            ip = ip.replace('http://','')
            h = ip.split(':')[0]
            p = ip.split(':')[1]
            print(h)
            print(p)
            telnetlib.Telnet(host= h,port= p,timeout=2)
            print("代理ip有效！")
            return True
        except:
            print("代理ip无效！")
            return False

    #打开这个网址，检测ip是否有效
    def checkip_(self,ip):
        url = 'http://icanhazip.com'
        proxy = {
            "http": ip,
            "https": ip,
        }
        print(proxy)
        try:
            print(1)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"}
            print(2)
            response = requests.get(url, proxies = proxy, headers = headers,timeout = 5)
            print(3)
            return response
        except Exception as e:
            print(str(e))
            return None

    def IPgetfrom89ip(self, page=10):
        h = parser.html_parser()
        for i in range(1, page):
            proxy_url = 'http://www.89ip.cn/' + str(i) + '.html'
            response = h.getnormalresponceofurl(proxy_url)
            # print(response.text)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            tag1 = soup.find_all('tr')
            for t in tag1:
                tds = t.find_all('td')
                # print(tds)
                ip = ''
                for td in tds[:2]:
                    # print(td.text)
                    ttext = td.text.split()[0]
                    if bool(re.search(r'\d', ttext)):
                        # print(td.text)
                        if len(ttext) > 5:
                            ip = ttext
                        else:
                            ip = ip + ':' + ttext
                            print(ip)
                            ip = "http://" + ip
                            if self.checkip(ip):
                                record = [ip, 2]
                                self.sqlman.Inserttosql_(self.db, self.tablename, record)


    def IPclean(self):
        self.sqlman.deletesql(self.db, self.tablename,'where flag < 2')
        # ips = self.sqlman.getsthfromsql(self.db,self.tablename,'ip',1,0,'where flag > 1')
        # for ip in ips:
        #     if not self.checkip(ip):
        #         self.punishthisproxy(ip)

if __name__ == '__main__':
    i = IpManager()
    #从数据库中选出可用的ip
    # proxies = i.getproxyfromipsql(10)
    # print(proxies)
    # i.IPclean()
    #从网络中获取新的ip
    i.IPgetfrom89ip(20)



