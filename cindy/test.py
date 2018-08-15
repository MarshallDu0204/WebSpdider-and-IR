import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re

def getHtml(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    headers = {'User-Agent':user_agent}
    #data = urllib.parse.urlencode(values)
    response_result = urllib.request.urlopen(url).read()
    html = response_result.decode('utf-8')
    return html

def requestCnblog(pagenum):
    prefix = ""
    if pagenum !=1:
        prefix = "sitehome/p/"+str(pagenum)
    url = "https://www.cnblogs.com/"+prefix
    result = getHtml(url)
    return result

def blogdecoder(pagenum):
    cnblogs = requestCnblog(pagenum)
    soup = BeautifulSoup(cnblogs,'html.parser')
    all_div = soup.find_all('div', attrs={'class': 'post_item_body'}, limit=20)
    blogs = []
    for item in all_div:
        temp = analyzeblog(item)
        blogs.append(temp)
    output(blogs)

def analyzeblog(item):
    result = {}
    title = find_all(item,'a','titlelnk')
    if title is not None:
        result["title"] = title[0].string
        result["link"] = title[0]["href"]
    summary = find_all(item,'p','post_item_summary')
    if summary is not None:
        result["summary"] = summary[0].text
    return result

def find_all(item,attr,c):
    return item.find_all(attr,attrs={'class':c},limit=1)

def output(list):
    with open("douban.txt", "a",encoding='utf-8') as f:
        for message in list:
            f.write(str(message)+"\n")
        f.write("\n+====================+\n")

if __name__ == '__main__':
    i=0;
    while i!=20:
        blogdecoder(i)
        print("pagenum ",i," done")
        i+=1
