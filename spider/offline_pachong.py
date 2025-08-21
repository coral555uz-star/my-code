from bs4 import BeautifulSoup
import json
import os 


def html2json(page,item):
    # 读取本地HTML文件
    with open(page, "r", encoding="utf-8") as f:
        html = f.read()
    # 解析HTML
    soup = BeautifulSoup(html, "html.parser")


    # 示例：提取所有链接
    for a in soup.find_all("div", class_="result-one"):
        p = a.find_all("p")
        item[p[0].text.strip()] = p[1].text.strip()


htmldata=r'/Users/zhouzhou/mycode/my-code/spider/96_texas'
item={}
for page in os.listdir(htmldata):
    html2json(os.path.join(htmldata, page),item)

with open("result.json", "a", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)