from bs4 import BeautifulSoup
import requests


rsp = requests.get("https://movie.douban.com/")
bsObj = BeautifulSoup(rsp.text,"lxml")

#uilist = soup.findAll("ul")
#print(soup.title.text)
#print(soup.body.text)

#for u in uilist:
#    print(u)

liList=bsObj.findAll("li",{"class":"ui-slide-item"})
for li in liList:
    ul = li.children
    for child in ul:
        print(child)

