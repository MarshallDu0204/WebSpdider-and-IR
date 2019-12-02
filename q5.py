f = open('C:\\Users\\Lenovo\\Desktop\\words.txt','r')
line = f.readlines()
freq = 1
dict = {}
for l in line:
    l = l.strip().split(' ')
    str = ''
    for words in l :
        words = words.lower()
        if words in dict:
            dict[words] = dict[words]+1
        else:
            dict[words] = freq
        word = "("+words+")"
        str = str+word
    #print(str)

print (sorted(dict.items(), key = lambda item:item[1],reverse=True))