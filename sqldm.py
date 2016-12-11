import pymysql
import sys
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.naive_bayes import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn import metrics
from sklearn.naive_bayes import BernoulliNB

cls_name = {'news_in':0, 'news_cn':1, 'ent':2, 'sports':3, 'finance':4, 'tech':5, 'games':6, 'edu':7, 'house':8, 'auto':9}

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', passwd='zxcvbnm123', port=3306, db='dm', charset='utf8')
    cur = conn.cursor()
    sql = 'select * from tfidf_2 where num<200000'
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    corpus = []
    cls = []
    #data = data[::2]
    
    for i in range(len(data)):
        corpus.append(data[i][1])
        cls.append(data[i][0])
    
    data = []
    print ('start tfidf')
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
    
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    y = []
    x = []
    corpus = []
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
         
        wdic = []
        
        for j in range(len(word)):
            
            wdic.append(weight[i][j])
        y.append(cls_name[cls[i]]) 
        x.append(wdic)
    cls = []
    '''
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
         
        wdic = {}
        
        for j in range(len(word)):
            
            wdic[j] = weight[i][j]
           
        
        y.append(cls_name[cls[i]]) 
        x.append(wdic)
    cls = []
    #print (x[0])
    
    print ('start svm')
    sys.path.append('C://Users/lll/Desktop/big data/dm/libsvm-3.21/python')
    from svmutil import *
    m = svm_train(y[::2], x[::2], '-h 0')
    p_label, p_acc, p_val = svm_predict(y[1::2], x[1::2], m)  
    '''
    train_y = y[::2]
    train_x = x[::2]
    test_y = y[1::2]
    test_x = x[1::2]
    y = []
    x = []
    print ('start')
    clf = MultinomialNB(alpha=0.01)
    clf.fit(train_x, train_y)
    pred_NB = clf.predict(test_x)
    print (len(pred_NB))

    for i in range(10):
        test_yi = test_y[i*9900:i*9900+9900]
        test_xi = test_x[i*9900:i*9900+9900]
        print (clf.score(test_xi, test_yi))

    
    