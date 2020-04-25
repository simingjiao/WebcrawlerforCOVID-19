import IpManager as ip
import SqlManager as sql
import Htmlparser as parser
import requests
import time
import Datacrawler.Keywords as key

# ***********基本信息请谨慎更改***********************************************************************************************
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"}
# ***************************************************************************************************************************

class SpiderMain(object):
    #构造函数中进行初始化
    def __init__(self):
        print("初始化成功")
    def geturl(self, keyword= '1',ts = '',te = '',region = '',subregion = ''):
        url = 'https://s.weibo.com/weibo'
        if keyword:
            url += '?q=' + keyword
        if region:
            url += '&region=custom:' + region
        # url += '&display=0&retcode=6102'
        if region and subregion:
            url +=':'+subregion

        if ts and te:
            url += '&timescope=custom:' + ts + ':' + te
        return url

    def createurl(self):
        #已添加前三个症状+12月-2月日期
        crawler = SpiderMain()
        k = key.keyword()
        s = sql.sqlmanager()
        cities = k.getregion()
        subcities = k.getsubregion()
        symptoms = k.getSymptoms()
        p = parser.html_parser()
        y = 2020
        m = 2
        de = 29
        h = 0
        for d in range(1,de):
            for h in [0,8,16]:
                ts,te = k.gett(y,m,d,h,8)
                print(ts)
                print(te)
                # for sym in symptoms:
                sym = symptoms
                for region in cities:
                    subregion = ''
                    # for subregion in subcities:
                    url = crawler.geturl(keyword=sym,region = str(region),subregion=str(subregion),ts=ts,te=te)
                    print(url)
                    s.Inserttosql_('xinguan','urlmanager',[sym,region,url,ts,te,0])
        for d in range(de,de+1):
            for h in [0,6,12]:
                ts,te = k.gett(y,m,d,h,6)
                print(ts)
                print(te)
                # for sym in symptoms:
                sym = symptoms
                for region in cities:
                    subregion = ''
                    # for subregion in subcities:
                    url = crawler.geturl(keyword=sym,region = str(region),subregion=str(subregion),ts=ts,te=te)
                    print(url)
                    s.Inserttosql_('xinguan','urlmanager',[sym,region,url,ts,te,0])
        # ts = '2019-11-30-18'
        # te = '2019-12-01-00'
        # sym = symptoms
        # for region in cities:
        #     subregion = ''
        #     # for subregion in subcities:
        #     url = crawler.geturl(keyword=sym, region=str(region), subregion=str(subregion), ts=ts, te=te)
        #     print(url)
        #     s.Inserttosql_('xinguan', 'urlmanager', [sym, region, url, ts, te, 0])

# crawler = SpiderMain()
# crawler.createurl()

s = sql.sqlmanager()
p = parser.html_parser()
tablename = 'sorethroat'
for i in range(1000):
    #and ts > "2019-11-12"
    url = s.getsthfromsql('xinguan','urlmanager','url',0,1,'where flag = 0 and keyword = "咽痛" and ts > "2020-02-25" ')
    maxpage = p.geturlsbyurl(url)
    if maxpage:
        pass
        maxpage = int(maxpage)
        for i in range(maxpage):
            i = int(i) + 1
            u = url + '&page=' + str(i)
            print(u)
            records = p.gettweetbyurl(u)
            if records:
                for r in records:
                    s.Inserttosql_('xinguan',tablename,r)
    else:
        u = url
        print(u)
        records = p.gettweetbyurl(u)
        if records:
            for r in records:
                s.Inserttosql_('xinguan', tablename, r)

def testcity():
    crawler = SpiderMain()
    cities = []
    index = []
    p = parser.html_parser()
    for region in range(11,101):
        url = crawler.geturl(region = str(region))
        print(url)
        time.sleep(1)
        city = p.getcitybyurl(url)
        if city:
            cities.append(city)
            index.append(region)
    print(cities)
    print(index)

def testsubcity():
    crawler = SpiderMain()
    p = parser.html_parser()
    k = key.keyword()
    regions = k.getregion()

    subregions = {}
    subindex = {}
    # subregions,subindex = k.getsubregion()
    # print(subregions)
    print(subindex)

    for region in regions:
        subregion = []
        index = []
        for sub in range(30):
            url = crawler.geturl(region=str(region),subregion = str(sub))
            print(url)
            time.sleep(0.5)
            city = p.getcitybyurl(url)
            print(city)
            if city and '~' in city:
                subregion.append(city)
                index.append(sub)
        subregions[region] = subregion
        subindex[region] = index
    print(subregions)
    print(subindex)