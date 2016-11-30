import pymysql
import sys
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

cls_name = {'news_in':0, 'news_cn':1, 'ent':2, 'sports':3, 'finance':4, 'tech':5, 'games':6, 'edu':7, 'house':8, 'auto':9}

def dm_main():
	conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
    cur = conn.cursor()
    sql = 'select * from tfidf'
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    corpus = []
    cls = []
    for i in range(len(data)):
    	corpus.append(data[1])
    	cls.append(data[0])
    data = []
    print 'start tfidf'
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
    
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    y = []
    x = []
    corpus = []
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
         
        wdic = {}
        
        for j in range(len(word)):
            
            wdic[j] = weight[i][j]
           
        
        y.append(cls_name[cls[i]]) 
        x.append(wdic)
    cls = []
    print 'start svm'
    sys.path.append('C://Users/lll/Desktop/big data/dm/libsvm-3.21/python')
    from svmutil import *
    m = svm_train(y[::2], x[::2])
    p_label, p_acc, p_val = svm_predict(y[1::2], x[1::2], m)  

if __name__ == '__main__':
	dm()