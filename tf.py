from __future__ import division
import math
from TF_IDF import GrobalParament
def TF_IDF_Compute(file_import_url_temp,file_export_url_temp,*words):
    data=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开  
        "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果  
        "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果  
        "我 爱 北京 天安门"]
    word_in_afile_stat={}
    word_in_allfiles_stat={}
    files_num=0
    while(data!=""):
        data_temp_1=[]
        data_temp_2=[]
        data_temp_1=data.split("\t") #file name and key words of a file     
        data_temp_2=data_temp_1[1].split(",")#key words of a file
        file_name=data_temp_1[0]
        data_temp_len=len(data_temp_2)
        files_num+=1
        for word in words:
            if word in data_temp_2:
                if not word_in_allfiles_stat.has_key(word):
                    word_in_allfiles_stat[word]=1
                else:
                    word_in_allfiles_stat[word]+=1
                
                if not word_in_afile_stat.has_key(file_name):
                    word_in_afile_stat[file_name]={}
                if not word_in_afile_stat[file_name].has_key(word):
                    word_in_afile_stat[file_name][word]=[]
                    word_in_afile_stat[file_name][word].append(data_temp_2.count(word))
                    word_in_afile_stat[file_name][word].append(data_temp_len)
        data=data_source.readline()
    data_source.close()
    if (word_in_afile_stat) and (word_in_allfiles_stat) and (files_num !=0):
        TF_IDF_result={}
        for filename in word_in_afile_stat.keys():
            TF_IDF_result[filename]={}
            for word in word_in_afile_stat[filename].keys():
                word_n=word_in_afile_stat[filename][word][0]
                word_sum=word_in_afile_stat[filename][word][1]
                with_word_sum=word_in_allfiles_stat[word]
                TF_IDF_result[filename][word]=((word_n/word_sum))*(math.log10(files_num/with_word_sum))
        TF_IDF_total={}
        for filename in TF_IDF_result.keys():
            TF_IDF_total[filename]=reduce(lambda x,y:x+y,TF_IDF_result[filename].values())       
        result_temp=[]
        result_temp=sorted(TF_IDF_total.iteritems(),key=lambda x:x[1],reverse=True)
        k=GrobalParament.result_file_num
        result=[]
        for item in result_temp:
            if k!=0:
                result.append(item[0])
                k-=1
            else:
                break       
    else:
        result=["None"]
    return result

if __name__ == '__main__':
    TF_IDF_Compute()