# -*- coding:utf-8 -*-

from trans_excel_to_mongo import IsoMongoCon
import requests
from bs4 import BeautifulSoup
import base64


headers = {
    "Cookie": 'bid=pU77NpKsK6A; ll="108288"; _ga=GA1.2.528162077.1510576908; push_noty_num=0; push_doumail_num=0; __utmv=30149280.15794; ap=1; _vwo_uuid_v2=6950D3929C87CE0724E4EC16D7CAED08|2315930244d8fc2678375d40be3be97e; ps=y; ue="sunsetmask@outlook.com"; dbcl2="157941904:25HEvb8KtMI"; ck=vbiL; __utmc=30149280; __utmz=30149280.1515475335.9.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ses.100001.4cf6=*; __utma=30149280.528162077.1510576908.1515475335.1515481268.10; __utmb=30149280.0.10.1515481268; __utma=223695111.528162077.1510576908.1515481268.1515481268.1; __utmb=223695111.0.10.1515481268; __utmc=223695111; __utmz=223695111.1515481268.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=3c32f504de79a878.1515481267.1.1515482097.1515481267.',
    "DNT": '1',
    "Host": "movie.douban.com",
    "Referer": "https://movie.douban.com/subject/2057171/?from=subject-page",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


with IsoMongoCon() as movie_collection:
    all_data = movie_collection.find({})
    last_refer = ""
    index = 1
    for movie in all_data:
        # 构建refer和获取html内容
        douban_url = movie['hyperlink']
        print('-- [{}] getting {} ...'.format(index, douban_url))
        headers["Referer"] = last_refer if last_refer else headers["Referer"]
        last_refer = douban_url
        response = requests.get(douban_url, headers=headers)
        
        # 解析图片链接
        soup = BeautifulSoup(response.content, 'html.parser')
        poster_url = soup.find("a", {"class": "nbgnbg"}).find("img")["src"]
        print(' | poster_url: {}'.format(poster_url))
        
        # 获取图片
        img_resp = requests.get(poster_url)

        # 写入文件
        img_name = poster_url.encode('ascii').split('/')[-1]
        with open('./poster_img/{}'.format(img_name), 'wb') as img:
            img.write(img_resp.content)

        # 存入数据库文件名字和url
        print(' | file name: {}'.format(img_name))
        movie_collection.update({'_id': movie['_id']}, 
            {"$set": {"poster_url": poster_url, "img_filename": img_name}})
        
        index += 1
