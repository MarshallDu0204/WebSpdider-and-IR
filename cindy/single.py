import porter
import time
start_time = time.process_time()
f = open('stopwords.txt','r')
lines = f.readlines()
stoplist = set()
filelist = []
dict = {}
p = porter.PorterStemmer()
for line in lines:
    line = line.strip()
    stoplist.add(line)
f1 = open('npl-doc-text.txt','r')
file = f1.read()
tempfilelist = file.split("/")
filelist = tempfilelist[0:len(tempfilelist)-3]
for file in filelist:
    file = file.strip()
    linelist = file.split("\n")
    templist = linelist[1:]
    worldlist = []
    dictword={}
    for line in templist:
        line = line.split(" ")
        for word in line:
            word = p.stem(word)
            if word not in stoplist and word !="":
                if word not in dictword.keys():
                    dictword[word] = 1
                else:
                    dictword[word] = dictword[word]+1
    dictword = sorted(dictword.items(),key = lambda item:item[1],reverse=True)
    dict[int(linelist[0])] = dictword
    if int(linelist[0])<=10:
        print(linelist[0],dict[int(linelist[0])])



end_time = time.process_time()
print( 'Time is{} seconds'.format(end_time - start_time))
