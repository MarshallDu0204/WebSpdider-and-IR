f = open('C:\\Users\\Lenovo\\Desktop\\index.txt','r')
lines = f.readlines()
dict = {}
for line in lines:
    list = line.split()
    templist = list[1:len(list)]
    newlist = [int(i) for i in templist]
    newlist.sort()
    dict[list[0]] = newlist


def mergeAnd(a,b):
    list = []
    x=0
    y=0
    while x<len(a) and y<len(b):
        if a[x]==b[y]:
          list.append(a[x])
          x=x+1
          y=y+1
        else:
            if a[x]<b[y]:
                x=x+1
            else:
                y=y+1
    return list


def mergeOr(a,b):
    list = []
    x=0
    y=0
    while x<len(a) or y<len(b):
        if x==len(a):
            x=x-1
            break
        elif y==len(b):
            y=y-1
            break
        else:
            if a[x]==b[y]:
                list.append(a[x])
                x+=1
                y+=1
            else:
                if a[x]<b[y]:
                    list.append(a[x])
                    x+=1
                else:
                    list.append(b[y])
                    y+=1

    if x==len(a)-1:
        while y<len(b):
            list.append(b[y])
            y+=1
    elif y==len(b)-1:
        while x<len(a):
            list.append(a[x])
            x+=1
    return list


def mergeNot(a,b):
    list = a
    x=0
    y=0
    while x<len(a) and y<len(b):
        if a[x]==b[y]:
            list.remove(a[x])
            x+=1
            y+=1
        else:
            if a[x]<b[y]:
                x+=1
            else:
                y+=1

    return list

input = input("Enter somethings to search")
info = input.split()
if 1 < len(info) <= 3:
    if info[1]=="or":
      value = mergeOr(dict[info[0]],dict[info[2]])
    elif info[1]=="and":
      value = mergeAnd(dict[info[0]],dict[info[2]])
    elif info[1]=="not":
      value = mergeNot(dict[info[0]],dict[info[2]])
    else:
        value ="Try again"
    print(value)
elif len(info) == 1:
    value = dict[info[0]]
    print(value)
else:
    print("Try again")


