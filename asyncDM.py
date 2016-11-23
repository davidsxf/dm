#coding= utf-8

import asyncio
import time
import aiohttp
import traceback
import re
#from bs4 import BeautifulSoup
#import requests
from lxml import html as HTML
import traceback
import json
import random
from page import page

#board_site = {'新闻': 'news', '娱乐': 'ent', '体育': 'sports', '财经': 'finance', '科技': 'tech', '游戏': 'games', '教育': 'edu', '房产': 'house', '汽车': 'auto'}
proxy = ['124.88.67.17:82', '1.82.216.135:80', '124.88.67.32:843',
         '1.82.216.134:80', '58.217.195.141:80', '122.72.18.160:80', '223.67.136.218:80', '120.52.21.132:8082', 
         '120.52.72.58:80', '120.52.72.56:80', '124.88.67.20:843', '124.88.67.54:843',
         '124.88.67.63:80']
         #'183.250.179.29:80', 
N = len(proxy) - 1


class task_url(object):
    @asyncio.coroutine
    def print_page(self, url, res):
        #print ('start')
        header = {
            'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'h-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'roll.news.qq.com',
            'Referer': 'http://roll.news.qq.com/index.htm?site=news&mod=1&date=2016-11-07&cata=',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
        try:
            #p = 'http://' + proxy[random.randint(0, N)]
            #p = 'http://124.88.67.17:82'
            #conn = aiohttp.ProxyConnector(p)
            response = yield from aiohttp.request('GET', url, headers=header)#, connector=conn)
            body =  yield from response.read()
            response.close()
            #print (url)
        except:
            traceback.print_exc()
            #print (url)
            return
        #print (1)
        try:
            data = json.loads(body.decode('gbk'))
        
            if data['data']:
                print (url)
                html = HTML.fromstring(data['data']['article_info'])
                url_li = html.xpath('//li')
                #print (len(url_li))
                #print (type(utl_type))
                for li in url_li:
                    try:
                        #url_type = li.xpath('span[@class="t-tit"]/text()')[0]
                    #except:
                    #    print (li.xpath('text()')[0]) 
                    #    url_type = 'CBA or NBA'
                    #print (str(url_type))
                        #if str(url_type):# != '[ 图片 ]' and str(url_type) != '[ &nbsp;彩票&nbsp; ]':
                    #    raise Exception
                    #if str(url_type) == '[国内]':
                    #if str(url_type) == '[国内]' or '[社会]':
                        #raise Exception
                        url_article = li.xpath('a/@href')
                        #print (url_article)
                        res.extend(url_article)
                    except:
                        traceback.print_exc()
                        pass
            else:
                pass
        except:
            traceback.print_exc()
            return
        #print (str(url_article[0]))
        '''
        for u in url_article:
            conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='test', charset='UTF8')
            cur = conn.cursor()
            name = str(u)
            sql = 'insert into user(num, name, url) values ("2", "2", "1")'#+name+', '+name+', '+str(u)+')'
            cur.execute(sql)
            sql = 'select * from user'
            cur.execute(sql)
            print (cur.fetchall())
            cur.close()
            conn.close() 
        '''

        
    
    def result(self, start, stop):
        loop = asyncio.get_event_loop()
        urls = []
        result = []
        site = 'games'
        for mon in range(start, stop):
            if mon<10:
                mon_time = '0' + str(mon)
            else:
                mon_time = str(mon)
            for i in range(1, 31):
                if i<10:
                    i_time = '0' + str(i)
                else:
                    i_time = str(i)
                for j in range(1, 5):
                    url1 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2016-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url2 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2015-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url3 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2014-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url4 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2013-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url5 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2012-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url6 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2011-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url7 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2010-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    urls.append(url1)
                    urls.append(url2)
                    urls.append(url3)
                    urls.append(url4)
                    urls.append(url5)
                    urls.append(url6)
                    urls.append(url7)
        #for i in range(2, 3):
        #    urls.append('http://sports.qq.com/l/isocce/xijia/laliganews_'+str(i)+'.htm')
        #u = ['http://roll.news.qq.com/interface/roll.php?0&cata=&site='+'sports'+'&date=2016-'+'03'+'-'+'21'+'&page='+'1'+'&mode=1&of=json']
        tasks = [self.print_page(url, result) for url in urls]
        #print (type(tasks), len(tasks))
        length = len(tasks)//400
        if not length:
            loop.run_until_complete(asyncio.wait(tasks))
        for t in range(length):
            task = tasks[t*400:t*400+400]
            loop.run_until_complete(asyncio.wait(task))
        #loop.close()
        return result


if __name__ == '__main__':
    print (time.ctime())
    end = []
    t = task_url()
    res = t.result(1, 13)

    print (len(res))
    print (len(list(set(res))))

    
    pag = page()
    pag.return_page(res, end)

    print (time.ctime())