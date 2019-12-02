import porter
import math
import time
starttime = time.process_time()
f = open('stopwords.txt','r')
lines = f.readlines()
stoplist = set()
filelist = []
dict = {}
p = porter.PorterStemmer()
query = {'logic','modulu','three'}
cleanquery = set()

for word in query:
    if word not in stoplist:
        word = p.stem(word)
        cleanquery.add(word)
print(cleanquery)

for line in lines:
    line = line.strip()
    stoplist.add(line)
f1 = open('npl-doc-text.txt','r')
file = f1.read()
tempfilelist = file.split("/")
filelist = tempfilelist[0:len(tempfilelist)-3]
filelenth = {}

for file in filelist:
    a=0
    file = file.strip()
    linelist = file.split("\n")
    templist = linelist[1:]
    worldlist = []
    dictword={}
    for line in templist:
        line = line.split(" ")
        for word in line:
            if word !="":
             a+=1
             word = p.stem(word)
             if word not in stoplist:
                if word not in dictword.keys():
                    dictword[word] = 1
                else:
                    dictword[word] = dictword[word]+1
    dict[int(linelist[0])] = dictword
    filelenth[int(linelist[0])]=a
tf = {}
tempidf = {}

for file in dict.keys():
    x = {}
    a=dict[file]
    for word in a.keys():
       if word in cleanquery:
          num = a[word]
          maxlen = 0
          for ab in a.values():
              if maxlen<ab:
                  maxlen=ab
          x[word] = num/maxlen
          if word in tempidf.keys():
              tempidf[word]=tempidf[word]+1
          else:
              tempidf[word]=1
    tf[file] = x
idf={}

for x in tempidf.keys():
    number = tempidf[x]
    number = len(filelenth)/number
    number = math.log2(number)
    idf[x] = number
print(idf)
tfidf = {}

for file in tf.keys():
    temp = {}
    x = tf[file]
    for word in x.keys():
        num = idf[word]
        num1 = x[word]
        num2 = num*num1
        temp[word] = num2
    tfidf[file] = temp
print(tfidf)
tfque = {}

for word in cleanquery:
    if word in tfque.keys():
        tfque[word]=tfque[word]+1
    else:
        tfque[word]=1
tfquery = {}
for word in tfque.keys():
    num = tfque[word]
    num = num/len(cleanquery)
    num = num/idf[word]
    tfquery[word] = num

sim ={}

for file in tfidf.keys():
    num=0
    x=tfidf[file]
    for word in x.keys():
        a = x[word]*tfquery[word]
        num = num+a
    doc = filelenth[file]
    que = len(cleanquery)
    sim[file] = num/(doc*que)
sim = sorted(sim.items(),key = lambda item:item[1],reverse = True)
print(sim)
endtime  = time.process_time()
print(endtime-starttime)