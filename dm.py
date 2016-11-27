import pynlpir
import pymysql
import traceback
import os  
import sys  
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

#board_site = {'新闻': 
f = open('stop_words_ch.txt', 'r')
stop_words = f.read()
stop_words += '腾讯\n'
f.close()


class_all = ['news_in', 'news_cn', 'ent', 'sports', 'finance', 'tech', 'games', 'edu', 'house', 'auto']
cls_name = {'news_in':0, 'news_cn':1, 'ent':2, 'sports':3, 'finance':4, 'tech':5, 'games':6, 'edu':7, 'house':8, 'auto':9}

def featureSel(cls, w_list, w_num, cls_w, all_w):
    pynlpir.open()
    word = []
    
    conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
    cur = conn.cursor()
    sql = 'select * from ' + cls + ' where num<22000'
    cur.execute(sql)
    text = cur.fetchall()
    cur.close()
    conn.close()

    #text = text[:10]
    print (len(text))
    cls_words = []
    all_words = []
    word_cls = []
    for te in text:
        
        

        try:
            t = pynlpir.segment(te[2])
            #w_list.append(t)
            words = []
            res = {}
            for w in t:
                
                if w[1] == 'noun' and w[0] not in stop_words:
                    words.append(w[0])
                    if w[0] not in cls_words:
                        cls_words.append(w[0])
                    
                    if w[0] not in res:
                        res[w[0]] = 0
                    res[w[0]] += 1
            word_cls.append(words)
            all_words.append(res)
                    #if w[0] not in words:
                    #    words.append(w[0])
            #num.append(res)

        except:
            pass
            #traceback.print_exc()
        #if words:
        #    w_list.append(words[:-1])
        #    w_num.append(cls)

    w_list.append(word_cls)
    all_w.append(all_words)
    cls_w.append(cls_words)
    #w_list.append(words[:-1])        
    pynlpir.close()
    
    #if words:
    #    w_list.append(words)
    #if num:
    #    w_num.append(num)
    

def dm():
    
    word_all = []
    word_num = []
    cls_w = []
    all_w = []
    for cls in class_all:
        featureSel(cls, word_all, word_num, cls_w, all_w)
    n = 0
    for i in range(len(class_all)):
        n += len(word_all[i])
    N = n
    print (N)
    corpus = []
    cls_corpus = []
    fea = []
    for i in range(len(class_all)):
        res = {}
        
        for w in cls_w[i]:
            num_else = 0
            len_else = 0
            a = 0
            b = 0
            c = 0      
            d = 0
            for k in all_w[i]:
                if w in k:
                    a += k[w]

            for i_no in range(i):
                num_else += len(word_all[i_no])
                for k in all_w[i_no]:
                    if w in k:
                        len_else += k[w]
                    
            for i_no in range(i+1, len(class_all)):
                num_else += len(word_all[i_no])
                for k in all_w[i_no]:
                    if w in k:
                        len_else += k[w]
                    
            c = len(cls_w[i]) - a
            d = num_else - b

            z1 = a*d - b*c
            z2 = (z1 * z1 * N * 1.0) /((a+c)*(a+b)*(b+d)*(c+d))
            res[w] = z2
        
        for re in sorted(res.items(), key=lambda x:x[1], reverse=True)[:500]:
            if re[0] not in fea:
                fea.append(re[0])
        print (class_all[i]+'col done!')
    print (len(fea))
    for i in range(len(class_all)):
        for val in word_all[i]:
            #print (len(val))
            words = ''
            for w in val:
                if w in fea:
                    words += w + ' '
            if words:
                corpus.append(words[:-1])
                cls_corpus.append(class_all[i])
    #print (len(corpus))
        print (class_all[i]+' is done!')
    return corpus, cls_corpus
    #print (len(cls_w), len(all_w))
    #return word_all, word_num, cls_w, all_w
    #print (word_all[0])
    #print (len(word_all))
    #print (sorted(word_num[0][5].items(), key=lambda x: x[1], reverse=True))
    #print (word_all, '\n', word_num)

if __name__ == '__main__':
    
    corpus, cls = dm()
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
    #print (tfidf)
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    y = []
    x = []
    f = open('set.txt', 'w')
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
        #print (u"-------这里输出第",i,u"类文本的词语tf-idf权重------")  
        wdic = {}
        f.write(str(cls_name[cls[i]])+' ')
        for j in range(len(word)):
            
            wdic[j] = weight[i][j]
            f.write(str(j)+':'+str(weight[i][j])+' ')
            #print (word[j],weight[i][j])
        f.write('\n')
        #dic = sorted(wdic.items(), key=lambda x:x[1], reverse=True)
        #print (len(wdic))
        
        y.append(cls_name[cls[i]]) 
        x.append(wdic)
    f.close()
    #print (x)
    #print (y, x)
    #print (y[0], len(x[0]))
    #print (y[-1], len(x[-1]))
    #os.chdir('C://Users/lll/Desktop/big data/dm/libsvm-3.21/python')
    #print (os.getcwd())
    sys.path.append('C://Users/lll/Desktop/big data/dm/libsvm-3.21/python')
    from svmutil import *
    m = svm_train(y[::2], x[::2])
    p_label, p_acc, p_val = svm_predict(y[1::2], x[1::2], m)  
    






def second_handle():
#函数用于进行第二层处理，获取TF和IDF；
#参数说明，database_name_list:需要处理的数据库列表
    database_name_list=["caijing","gongyi","jiankang","jiaoyu","junshi","keji","lvyou","nvxing","wenshi","yule"];
    every_file_list={};#建立存放单词的字典，统计每个词出现的次数,即包含该单词的文章篇数
    f=0;
    for database_name in database_name_list:
        print("database_name:"+database_name)
        get_data(every_file_list,database_name);
    print(len(every_file_list));
    for database_name in database_name_list:
        file_num=1;#表编号;
        while file_num<20000:#对每个数据库中的所有文件进行处理，但找IDF值只在每个数据库的前10000篇找
            words_IDF_dic={};
            table_name = database_name + str(file_num);  # 将要处理的表名
            get_words(database_name,table_name,words_IDF_dic);
            #print(words_IDF_dic);

            get_IDF(every_file_list,words_IDF_dic);
            for key in words_IDF_dic:
                TF=float(words_IDF_dic[key][0])/float(words_IDF_dic[key][1]);
                TF_IDF=TF*math.log(100000/float(words_IDF_dic[key][2]+1));
                words_IDF_dic[key][3]=TF_IDF;
            if f==0:
                print(words_IDF_dic);
                f+=1;
                #input("请输入：");
            print(database_name+":"+table_name);
            file_num+=1;
            update_table_with_IDF(database_name,table_name,words_IDF_dic);