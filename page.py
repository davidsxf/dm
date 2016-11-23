import asyncio
import json
import aiohttp
from lxml import html as HTML
#import requests
import random
import traceback
import pymysql

header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'news.qq.com',
            'Referer': 'http://roll.news.qq.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
    

us = ['http://ent.qq.com/a/20161111/026252.htm', 'http://ent.qq.com/a/20161111/026658.htm', 
      'http://ent.qq.com/a/20161111/026207.htm', 'http://news.qq.com/a/20161118/001449.htm',
      'http://news.qq.com/a/20161118/001363.htm', 'http://news.qq.com/a/20161118/000633.htm',
      'http://news.qq.com/a/20161117/043487.htm', 'http://news.qq.com/a/20161117/043348.htm',
      'http://news.qq.com/a/20161117/042390.htm', 'http://news.qq.com/a/20161118/008272.htm',
      'http://news.qq.com/a/20161118/009324.htm', 'http://news.qq.com/a/20161118/004480.htm']

proxy = ['124.88.67.17:82', '1.82.216.135:80', '124.88.67.32:843',
         '1.82.216.134:80', '58.217.195.141:80', '122.72.18.160:80', '223.67.136.218:80', '120.52.21.132:8082', 
         '120.52.72.58:80', '120.52.72.56:80', '124.88.67.20:843', '124.88.67.54:843',
         '124.88.67.63:80']

#'183.250.179.29:80', 
#'118.180.15.151:8102'  124.88.67.17:82',      , '221.226.82.130:8998'          120.52.72.56:80
N = len(proxy) - 1

class page(object):
    @asyncio.coroutine
    def get_page(self, url, cnt):
        #print ('start')
        #print ('next')
        article = ''
        art_text = ''

        try:
            #p = 'http://' + proxy[random.randint(0, N)]
            p = 'http://' + proxy[1] 
            #print (p)
            conn = aiohttp.ProxyConnector(proxy=p)
            request = yield from aiohttp.request('GET', url, connector=conn)
            page = yield from request.read()
            request.close()
            #print (len(cnt))
            pro = p
        except:
            traceback.print_exc()
            #print (len(cnt), p)
            return 0
        try:
            html = HTML.fromstring(page.decode('gbk'))
        except:
            return 0
            #open('test.txt', 'w').write(url+' '+'gbk'+'\n')
        try:
            article_all = html.get_element_by_id("Cnt-Main-Article-QQ") 
            #print (article_all, url)
            #hd = article_all.xpath('div[@class="hd"]/h1[1]/text()')[0]
            #bd = article_all.xpath('div[@class="bd"]')[0]
            #bd = html.find_class('bd')[0]
            #text = bd.xpath('//div[@class="Cnt-Main-Article-QQ"]/p[@style="TEXT-INDENT: 2em"]/text()')
            text = article_all.xpath('./p[@style="TEXT-INDENT: 2em"]/text()')
            
            text1 = article_all.xpath('./p[@style="TEXT-INDENT:2em"]/text()')
            for p in text:
                art_text += str(p)
            for p in text1:
                art_text += str(p)
            #print (art_text)
            #conn =  pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
            #cur  = conn.cursor()
            #sql = "insert into news_in values ("++",,)"
            
            if len(art_text)>100:# and '彩票' not in art_text:
                if not len(cnt)%400:
                    print (len(cnt))
                art_text = art_text.replace("‘", "")
                art_text = art_text.replace("“", "")
                #print (art_text, url)
                cnt.append(url)
                #print (len(cnt), pro)
                
                conn =  pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
                cur  = conn.cursor()
                sql = "insert into games values ("+str(len(cnt)-1)+",'"+url+"','"+art_text+"')"
                cur.execute(sql)
                cur.close()
                conn.commit()
                conn.close()
                
                #print (len(cnt))
                #print ('write!')
            else:
                pass
                #print (url)
        except IndexError:
            #traceback.print_exc()
            #print (url, 'no bd')
            return
        except:
            traceback.print_exc()
            return 0
            #open('test.txt', 'w').write(url+'\n')
        #print (len(text))
        #print (text)
        #print (art_text)

    def return_page(self, urls, tmp):
        print (len(urls))
        #print (urls)
        loop = asyncio.get_event_loop()
        tasks = [self.get_page(url, tmp) for url in urls]
        length = len(tasks)//100
        if length == 0:
            loop.run_until_complete(asyncio.wait(tasks))
        else:
            for t in range(length):
                try:
                    task = tasks[t*100: t*100+100]
                except:
                    task = tasks[t*100:]
                try:
                    loop.run_until_complete(asyncio.wait(task))
                except:
                    pass
        loop.close()
        print (len(tmp))

if __name__ == '__main__':
    task = page()
    l = []
    task.return_page(us, l)








