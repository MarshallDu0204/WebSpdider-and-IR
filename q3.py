f = open('C:\\Users\\Lenovo\\Desktop\\words.txt','r')
line = f.readlines()
for l in line:
    l = l.strip().split(' ')
    str = ''
    for words in l :
        words = words.lower()
        word = "("+words+")"
        str = str+word
    print(str)