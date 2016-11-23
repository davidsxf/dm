f = open('', 'r')
stop_words = f.read()
f.close()
word_all = []
word_num = []
class_all = []

def featureSel(cls, w_list, w_num):
    pynlpir.open()
    num = []
    words = []
    conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', db='dm', charset='utf8')
    cur = conn.cursor()
    sql = 'select * from' + cls
    text = cur.execute(sql)
    cur.close()
    conn.close()
    for te in text:
        t = pynlpir.segment(te[3])
        res = {}
        for w in t:
            if t[1] == 'noun' and t[0] not in stop_words:
                if t[0] not in res:
                    res[t[0]] = 0
                res[t[0]] += 1
                if t[0] not in words:
                    words.append(t[0])
        num.append(res)
    w_list.append(words)
    w_num.append(num)
    

def dm():
    words_class = {}
    for c in class_all:
        featureSel(c, word_all, word_num)

    for i in range(10):
