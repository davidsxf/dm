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
#import pymysql
from page import page

#board_site = {'新闻': 'news', '娱乐': 'ent', '体育': 'sports', '财经': 'finance', '科技': 'tech', '游戏': 'games', '教育': 'edu', '房产': 'house'}

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
            response = yield from aiohttp.request('GET', url, headers=header, connector=None)
            body =  yield from response.read()
            response.close()
        except:
            traceback.print_exc()
            print (url)
            return
        #print (1)
        try:
            data = json.loads(body.decode('gbk'))
        
            if data['data']:
                #print (data)
                html = HTML.fromstring(data['data']['article_info'])
                url_li = html.xpath('//li')
                #print (type(utl_type))
                for li in url_li:
                    url_type = li.xpath('span[@class="t-tit"]/text()')[0]
                    #print (str(url_type))
                    #if str(url_type) == '[图片]':
                    #    raise Exception
                    if str(url_type) == '[国际]':
                    #if str(url_type) == '[国内]' or '[社会]':
                        #raise Exception
                        url_article = li.xpath('a/@href')
                        res.extend(url_article)
            else:
                pass
        except:
            pass
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
        site = 'news'
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
                for j in range(1, 6):
                    url1 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2016-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url2 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2015-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    url3 = 'http://roll.news.qq.com/interface/roll.php?0&cata=&site='+site+'&date=2014-'+mon_time+'-'+i_time+'&page='+str(j)+'&mode=1&of=json'
                    urls.append(url1)
                    urls.append(url2)
                    urls.append(url3)
        #for i in range(2, 3):
        #    urls.append('http://sports.qq.com/l/isocce/xijia/laliganews_'+str(i)+'.htm')
        tasks = [self.print_page(url, result) for url in urls]
        print (type(tasks), len(tasks))
        length = len(tasks)//400
        for t in range(length):
            task = tasks[t*400:t*400+400]
            loop.run_until_complete(asyncio.wait(task))
        #loop.close()
        return result


if __name__ == '__main__':
    print (time.ctime())
    end = []
    t = task_url()
    res = t.result(11, 12)

    print (len(res))
    print (len(list(set(res))))

    
    pag = page()
    pag.return_page(res[:20], end)
    print (time.ctime())