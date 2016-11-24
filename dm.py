import pynlpir
import pymysql
import traceback

#board_site = {'新闻': 
f = open('stop_words_ch.txt', 'r')
stop_words = f.read()
f.close()
word_all = []
word_num = []
class_all = ['news_in', 'news_cn', 'ent', 'sports', 'finance', 'tech', 'games', 'edu', 'house', 'auto']

def featureSel(cls, w_list, w_num):
    pynlpir.open()
    num = []
    words = []
    conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
    cur = conn.cursor()
    sql = 'select * from ' + cls
    cur.execute(sql)
    text = cur.fetchall()
    cur.close()
    conn.close()

    text = text[:10]
    print (len(text))
    
    for te in text:
       
        try:
            t = pynlpir.segment(te[2])
            #w_list.append(t)
            
            res = {}
            for w in t:
                if w[1] == 'noun' and w[0] not in stop_words:
                    if w[0] not in res:
                        res[w[0]] = 0
                    res[w[0]] += 1
                    if w[0] not in words:
                        words.append(w[0])
            num.append(res)
            
        except:
            pass
            #traceback.print_exc()
            

    if words:
        w_list.append(words)
    if num:
        w_num.append(num)
    

def dm():
    words_class = {}

    featureSel(class_all[0], word_all, word_num)
    #print (word_num)
    print (sorted(word_num[0][5].items(), key=lambda x: x[1], reverse=True))
    #print (word_all, '\n', word_num)

if __name__ == '__main__':
    dm()
