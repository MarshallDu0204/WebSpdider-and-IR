import re
import porter
import time
import os
import math
import sys
start_time = time.process_time()
total = []
averageW = []
averageT = []
averageA = []
averageB = []
result = {}
relevance = {}
p = porter.PorterStemmer()
f1 = open('stopwords.txt','r')
lines = f1.readlines()
stoplist = set()
for line in lines:
    line = line.strip()
    stoplist.add(line)

def preprocess():
    f = open('cranfield_collection.txt', 'r')
    file = f.read()
    filelist = file.split(".I")
    filelist = filelist[1:len(filelist)]
    newfilelist = []
    avgW = 0
    avgT = 0
    for file in filelist:
        newfile = re.split(r".T|.A|.B|.W", file)
        if len(newfile)>5:
            newfile = newfile[0:5]
        words = re.split(r"\n| ", newfile[4])
        list = []
        for word in words:
            if word not in stoplist and word != "" and word != "." and word != "..":
                word = p.stem(word)
                list.append(word)
        avgW = avgW + len(list)
        newfile[4] = list
        words1 = re.split(r"\n| ", newfile[1])
        list1 = []
        for word in words1:
            if word not in stoplist and word != "" and word != "." and word != "..":
                word = p.stem(word)
                list1.append(word)
        avgT = avgT + len(list1)
        newfile[1] = list1
        newfile[0] = newfile[0].strip()
        newfile[2] = newfile[2].strip()
        newfile[3] = newfile[3].strip()
        newfilelist.append(newfile)
    avgW = avgW / len(filelist)
    avgT = avgT / len(filelist)

    filename = "Index.txt"
    with open(filename,'w') as f1:
        for file in newfilelist:
            i = ".I " + file[0]+"\n"
            t = ".T\n" + " ".join(file[1])+"\n"
            a = ".A\n" + file[2]+"\n"
            b = ".B\n" + file[3]+"\n"
            w = ".W\n" + " ".join(file[4])+"\n"
            numW = len(file[4])
            numW = ".numW\n"+str(numW)+"\n"
            numT = len(file[1])
            numT = ".numT\n" +str(numT)+"\n"
            f1.write(i)
            f1.write(t)
            f1.write(a)
            f1.write(b)
            f1.write(w)
            f1.write(numW)
            f1.write(numT)



newquery1 = {}

def queryprocess():
    f = open('cranfield_queries.txt', 'r')
    newquery = f.read()
    newquery = newquery.split(".I")
    newquery = newquery[1:len(newquery)]

    for file in newquery:
        file = file.split(".W")
        file[0] = file[0].strip()
        file[1] = file[1].strip()
        newquery1[file[0]] = file[1]

def process():
    f=""
    if os.path.exists("Index.txt") :
        f = open('Index.txt', 'r')
    else:
        preprocess()
        f =  open('Index.txt', 'r')
    file = f.read()

    file = file.split(".I")
    filelist = file[1:len(file)]
    sumT = 0
    sumA = 0
    sumB = 0
    sumW = 0
    for file in filelist:

        x = set()
        y = {}

        newfile = re.split(r".T|.A|.B|.W|.numW|.numT", file)
        newfile[1] = newfile[1].split(" ")
        newfile[1][0]=newfile[1][0].strip()
        newfile[1][len(newfile[1])-1] = newfile[1][len(newfile[1])-1].strip()
        newfile[4] = newfile[4].split(" ")
        newfile[4][0] = newfile[4][0].strip()
        newfile[4][len(newfile[4]) - 1] = newfile[4][len(newfile[4]) - 1].strip()
        lenthT = len(newfile[1])
        sumT = sumT + lenthT
        lenthW = len(newfile[4])
        sumW = sumW + lenthW
        a = set()
        b = {}
        for word in newfile[4]:
            if word in b.keys():
                b[word] = b[word]+1
            else:
                b[word] = 1
            a.add(word)
        newfile[4]=a
        newfile.append(b)
        a1 = set()
        b1 = {}
        for word in newfile[1]:
            if word in b1.keys():
                b1[word] = b1[word]+1
            else:
                b1[word] = 1
            a1.add(word)
        newfile[1] =a1
        newfile.append(b1)
        newfile.append(lenthT)
        newfile.append(lenthW)
        newfile[0]=newfile[0].strip()
        newfile[2]=newfile[2].strip()
        newfile[2] = re.split(r",|and",newfile[2])
        x = set()
        for a in newfile[2]:
            x.add(a)
        newfile[2]=x
        newfile[3]=newfile[3].strip()
        newfile[3] = newfile[3].split(" ")
        x1 = set()
        for a in newfile[3]:
            x1.add(a)
        newfile[3]=x1
        lenA = len(newfile[2])
        sumA= sumA+lenA
        lenB = len(newfile[3])
        sumB = sumB+lenB
        total.append(newfile)
    sumT = sumT/len(total)
    averageT.append(sumT)
    sumA = sumA/len(total)
    averageA.append(sumA)
    sumB = sumB/len(total)
    averageB.append(sumB)
    sumW = sumW/len(total)
    averageW.append(sumW)

def query1(index,query):
    value = {}
    query = query.split(" ")
    cleanquery = set()
    for word in query:
        if word not in stoplist and word != "" and word != ".":
            word = p.stem(word)
            cleanquery.add(word)
    querynumberW = {}
    querynumberT = {}
    querynumberA = {}
    querynumberB = {}
    for newfile in total:
        for word in cleanquery:
            if word in newfile[4]:
                if word in querynumberW.keys():
                    querynumberW[word] = querynumberW[word]+1
                else:
                    querynumberW[word]=1


            if word in newfile[1]:
                if word in querynumberT.keys():
                    querynumberT[word]=querynumberT[word]+1
                else:
                    querynumberT[word]=1

            if word in newfile[2]:
                if word in querynumberA.keys():
                    querynumberA[word]=querynumberA[word]+1
                else:
                    querynumberA[word]=1

            if word in newfile[3]:
                if word in querynumberB.keys():
                    querynumberB[word]=querynumberB[word]+1
                else:
                    querynumberB[word]=1

        qw = {}
        qt = {}
        qa = {}
        qb = {}
        for word in newfile[4]:
            if word in cleanquery:
                qw[word] = newfile[7][word]

        for word in newfile[1]:
            if word in cleanquery:
                qt[word] = newfile[8][word]

        for word in newfile[2]:
            if word in cleanquery:
                qa[word] = 1

        for word in newfile[3]:
            if word in cleanquery:
                qb[word] = 1

        numW = 0
        if len(qw)!=0:
            for word in qw:
                f = int(qw[word])
                k = 1
                b = 0.75
                numW = numW + (f * (1 + k) / (f + k * ((1 - b) + b * newfile[10] / averageW[0])))*math.log((len(total) - querynumberW[word] + 0.5) / (querynumberW[word] + 0.5),2)

        numT = 0
        if len(qt)!=0:
            for word in qt:
                f = int(qt[word])
                k = 1
                b = 0.75
                numT = numT + (f * (1 + k) / (f + k * ((1 - b) + b * newfile[9] / averageT[0]))) * math.log((len(total) - querynumberT[word] + 0.5) / (querynumberT[word] + 0.5),2)

        numA = 0
        if len(qa)!=0:
            for word in qa:
                f = int(qa[word])
                k = 1
                b = 0.75
                numA = numA + (f * (1 + k) / (f + k * ((1 - b) + b * len(newfile[2]) / averageA[0]))) * math.log((len(total) - querynumberA[word] + 0.5) / (querynumberA[word] + 0.5),2)

        numB = 0
        if len(qb)!=0:
            for word in qb:
                f = int(qb[word])
                k = 1
                b = 0.75
                numB = numB + (f * (1 + k) / (f + k * ((1 - b) + b * len(newfile[3]) / averageB[0]))) * math.log((len(total) - querynumberB[word] + 0.5) / (querynumberB[word] + 0.5),2)


        value[newfile[0]]=numW+(numT)*1.2+(numA)*1.5+numB*0.5
        if newfile[0]=="1400":
            value =  sorted(value.items(),key = lambda item:item[1],reverse = True)
            value = value[0:15]
            if index == "000":
                i=1
                for x in value:
                    print(i,x)
                    i+=1
                value = {}
            else:
                result[index]=value



def evaluation():
    process()
    queryprocess()
    for x in newquery1.keys():
        query1(x,newquery1[x])
    with open("evaluation_output.txt", 'w') as f:
        for value in result:
           a = ".I "+value+"\n"
           b = ""
           r = 1
           for index in result[value]:
               b = b+".D "+index[0]+" .R "+str(r)
               r+=1
           b = b+"\n"
           f.write(a)
           f.write(b)
    with open("cranfield_relevance.txt",'r') as f1:
        f1 = f1.read()
        relevance1 = f1.split("-1")
        i=1
        for r in relevance1:
            a = {}
            r = r.split("\n")
            for r1 in r:
                if r1 !="":
                    r1 = r1.split(" ")
                    if len(r1)==2:
                        r1[0]="0"
                        r1[1]="0"
                        r1.append("0")
                    if len(r1)==3:
                        r1[2]="1"
                    if len(r1)==4:
                        r1 = r1[0:3]
                    if len(r1)==5:
                        x = r1[3]
                        r1 = r1[0:3]
                        r1[2] = x
                    a[r1[1]] = r1[2]
            relevance[i]=a
            i+=1
        a = 1
        ap = 0
        ap1 = 0
        ap10 = 0
        amap = 0
        aidcg10 = 0
        for r in result:
            p = 0
            p10 = 0
            map = 0
            idcg10 = 0
            g = []
            ig = []
            cg = []
            dcg = []
            idcg = []
            s = 1
            sort = sorted(relevance[a].items(),key = lambda item:item[1],reverse=True)

            for x in result[r]:
                g.append(0)
                if (s)>len(sort):
                    ig.append(0)
                if (s)<=len(sort):
                    ig.append(int(sort[s-1][1]))
                if x[0] in relevance[a]:
                    g[len(g)-1]=int(relevance[a][str(x[0])])
                    p+=1
                    map = p/s
                    if s==1:
                        dcg.append(1)
                    if s!=1:
                        x1 = dcg[len(dcg)-1]+g[len(g)-1]/math.log(s,2)
                        dcg.append(x1)
                if x[0] not in relevance[a]:
                    if s==1:
                        dcg.append(0)
                    if s != 1:
                        dcg.append(dcg[len(dcg)-1])
                if s<=10 and x[0] in relevance[a]:
                    p10+=1
                if s==1:
                    idcg.append(ig[0])
                    cg.append(g[0])
                if s!=1:
                    x1 = cg[s-2]+g[s-1]
                    cg.append(x1)
                    y1 = idcg[len(idcg)-1]+ig[s-1]/math.log(s,2)
                    idcg.append(y1)
                s+=1
            precision = p/len(result[r])
            ap = ap+precision
            recall = p/len(relevance[a])
            ap1 = ap1+recall
            p10 = p10/10
            ap10  = ap10+p10
            map = map+map/10
            amap=amap+map
            idcg10 = idcg10+dcg[9]/idcg[9]
            aidcg10 = aidcg10+idcg10
            a +=1
        ap = ap/225
        ap1 = ap1/225
        ap10  =ap10/225
        amap =amap/225
        aidcg10 = aidcg10/225
        print( "precision: ", ap, "\nrecall: ", ap1, "\np10: ", ap10, "\nmap: ", amap, "\nidcg10: ",aidcg10)
def query(words):
    query1("000",words)

if __name__ == '__main__':
    if sys.argv[1]=="-m" and sys.argv[2]=="query":
        process()
        name = ""
        while name != "exit":
            name = input("please enter your query: \n")
            if name == "exit":
                break
            query(name)
    if sys.argv[1]=="-m" and sys.argv[2]=="evaluation":
        evaluation()

end_time = time.process_time()
print( 'Time is{} seconds'.format(end_time - start_time))