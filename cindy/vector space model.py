import porter
import  math
p = porter.PorterStemmer()
f = open('stopwords.txt','r')
lines = f.readlines()
stoplist = []
for line in lines:
    line = line.strip()
    stoplist.append(line)
documents = {
'd1':['Shipment', 'of', 'gold', 'damaged', 'in', 'a', 'fire'],
'd2':['Delivery', 'of', 'silver', 'arrived', 'in', 'a', 'silver', 'truck'],
'd3':['Shipment', 'of', 'gold', 'arrived', 'in', 'a', 'large', 'truck']
}
documentlist = []
for document in documents.keys():
    vsmD = {}
    docId = int(document[1])
    templist = documents[document]
    list = []
    for word in templist:
        word = word.lower()
        word = p.stem(word)
        if word not in stoplist:
           list.append(word)
           if word not in vsmD.keys():
               vsmD[word] = 1
    documents[document] = list
    documentlist.append(vsmD)
    documentlist[docId-1]=vsmD
query = ['gold', 'silver', 'truck']
vsmQ = {}
for word in query:
    if word not in vsmQ.keys():
        vsmQ[word]=1

print(documentlist)
print(vsmQ)
array = []
i=0
sim = {}
while(i<len(documentlist)):
    j=0
    for key in vsmQ.keys():
        if key in documentlist[i].keys():
            j+=1
    lenQ = math.sqrt(len(vsmQ))
    lenD = math.sqrt(len(documentlist[i].values()))
    array.append(1)
    array[i] = j/(lenQ*lenD)
    x = 'd'+str(i+1)
    sim[x] = array[i]
    i+=1
sim = sorted(sim.items(),key = lambda item:item[1],reverse=True)
print(sim)


