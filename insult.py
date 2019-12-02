from pandas import *
from numpy import *

def createDataSet():           #创造训练集
    postingList= [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],  # 切分的词条
               ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
               ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
               ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
               ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
               ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid'],
               ['you','are','shit','ass'],
               ['shit','idiot'],
               ['ass','hole','bull'],
               ['you','look','pretty','nice']]

    classVec = [0, 1, 0, 1, 0, 1 , 1 , 1 , 1 , 0 ]
    return postingList,classVec

def createVocaList(postingList):     #将list格式的训练集中的所有出现过的元素存为set
    vocalSet=set([])
    for line in postingList:
        vocalSet=vocalSet|set(line)
    return vocalSet

def DataSet2Vec(vocalSet,input):   #将input转化为向量
    vocalList=list(vocalSet)
    num_vocal=len(vocalList)
    num_lines=len(input)
    returnVec=zeros((num_lines,num_vocal))
    for i in range(num_lines):
        for j in range(len(input[i])):
            if input[i][j] in vocal_Set:
                t=input[i][j]
                returnVec[i][vocalList.index(t)]=1
            else:
                print("输入的句子中有set未曾出现过的元素")
    return returnVec


def train_dataset(vocal_Vector,classVec):
    num_lines=len(vocal_Vector)
    num_words_in_line=len(vocal_Vector[0])
    count_abusive_list=zeros(num_words_in_line)
    count_no_abusive_list=zeros(num_words_in_line)
    num_Abusive=sum(classVec)   #侮辱性的句子的数量
    pAbusive=num_Abusive/float(num_lines)    #侮辱性句子的概率
    for i in range(num_lines):
        if classVec[i]==1: #该行是侮辱性的
            count_abusive_list=count_abusive_list+vocal_Vector[i]
        else:
            count_no_abusive_list = count_no_abusive_list + vocal_Vector[i]
    list_pAbusive=-log((count_abusive_list+0.1)/(sum(count_abusive_list)+0.1))
    list_pnoAbusive=-log((count_no_abusive_list + 0.1) / (sum(count_no_abusive_list) + 0.1))
    # print("在已经选出侮辱性句子的情况下，每个词属于侮辱性的概率的list是%s"%list_pAbusive)
    # print("在已经选出非侮辱性句子的情况下，每个词属于非侮辱性的概率的list是%s" % list_pnoAbusive)
    # print("所有的句子中，侮辱性句子的比例即概率为%s"%pAbusive)
    return list_pAbusive,list_pnoAbusive,pAbusive


def classify(voc_to_list,list_pAbusive,list_pnoAbusive,pAbusive):
    num=len(voc_to_list[0])
    list_Abusive=voc_to_list*list_pAbusive
    list_no_Abusive=voc_to_list*list_pnoAbusive
    # print("list_Abusive是%s"%list_Abusive)
    # print("list_no_Abusive%s"%list_no_Abusive)
    a=0.0
    b=0.0
    for i in range(num):
        if list_Abusive[0][i]>0:
            a=list_Abusive[0][i]+a
        if list_no_Abusive[0][i]>0:
            b=list_no_Abusive[0][i]+b
    if (a*pAbusive)<=(b*(1-pAbusive)):
        print("属于侮辱类")
    else:
        print("不是侮辱类")



postingList,classVec=createDataSet() #生成数据集

vocal_Set=createVocaList(postingList)  #将训练机转化为set格式

returnVec=DataSet2Vec(vocal_Set,postingList)   #将输入的postinglist根据set转化为向量

list_pAbusive,list_pnoAbusive,pAbusive=train_dataset(returnVec,classVec)  #输入训练集合，训练朴素贝叶斯模型

input_one=[['stupid', 'garbage','idiot','shit']]  #测试1：侮辱类
print(type (input_one))
input_one_vector=DataSet2Vec(vocal_Set,input_one)
classify(input_one_vector,list_pAbusive,list_pnoAbusive,pAbusive)


input_two=[['you','shit','ass']]    #测试2：非侮辱类
input_two_vector=DataSet2Vec(vocal_Set,input_two)
classify(input_two_vector,list_pAbusive,list_pnoAbusive,pAbusive)

input_three=[['worthless', 'stupid', 'dog']]    #测试3：
input_three_vector=DataSet2Vec(vocal_Set,input_three)
classify(input_three_vector,list_pAbusive,list_pnoAbusive,pAbusive)