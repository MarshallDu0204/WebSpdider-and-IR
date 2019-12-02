f = open('C:\\Users\\Lenovo\\Desktop\\words.txt','r')
line = f.readlines()
for l in line:
    l = l.split()
    print(l)