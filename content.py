import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

def getHtml(url):
    user_agent  ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    headers = {'User_Agent':user_agent}
    response_result = urllib.request.urlopen(url).read()
    html = response_result.decode('utf-8')
    return html

def requestWebsite(pagenum):
    postfix  =""
    if pagenum!=1:
        postfix = "sitehome/p/"+str(pagenum)
    url = "https://www.cnblogs.com/"+postfix
    result = getHtml(url)
    return result

def blogdecoder(pagenum):
    cnblogs = requestWebsite(pagenum)
    soup = BeautifulSoup(cnblogs,'html.parser')
    all_links = soup.find_all('a', attrs={'class': 'titlelnk'}, limit=20)
    contents = []
    code = []
    for link in all_links:
        temp,codetemp = linkDecoder(link['href'])
        contents.append(temp)
        code.append(codetemp)
    output(contents,pagenum)
    outputcode(code,pagenum)

def linkDecoder(url):
    content = getHtml(url)
    soup = BeautifulSoup(content, 'html.parser')
    article = soup.find_all('div',attrs = {'id':'cnblogs_post_body'},limit = 1)
    codes = soup.find_all('div',attrs = {'class':'cnblogs_code'},limit  =10)
    codelist = []
    for item in codes:
        temp = item.find_all('span')
        for item in temp:
            codelist.append(item.get_text())
    body = article[0].find_all('p',attrs = {},limit = 30)
    list = []
    for p in body:
        list.append(str(p))
    return list,codelist

def output(content,pagenum):
    with open("article.txt", "a",encoding='utf-8') as f:
        f.write(str(pagenum+1)+"\n+====================+\n")
        for message in content:
            f.write(str(message)+"\n")
        f.write("\n+====================+\n")

def outputcode(code,pagenum):
    with open("code.txt", "a",encoding='utf-8') as f:
        f.write(str(pagenum)+"\n+====================+\n")
        for message in code:
            f.write(str(message)+"\n")
        f.write("\n+====================+\n")

if __name__ == '__main__':
    i=0
    while i!=20:
        blogdecoder(i)
        print(i+1,"done")
        i+=1

