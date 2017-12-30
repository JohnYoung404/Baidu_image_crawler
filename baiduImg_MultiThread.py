#!/usr/bin/python  
#coding:utf-8
import http.client
import urllib
from urllib.request import urlopen
from urllib.parse import quote
import json
import re
import os
import sys
import threading
import socket

page = 0
imgCount = 0
ulist = []
doneCount = 0
socket.setdefaulttimeout(20)

def request(searchword):
    if not os.path.exists('./' + searchword):
        os.mkdir('./' + searchword) 
    while 1:
        try:
            if(doneCount >= 100):
                sys.exit()
            global page
            conn = http.client.HTTPConnection('image.baidu.com')  
            request_url ='/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word='+quote(searchword)+'&cg=girl&rn=60&pn='+str(page)
            headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0','Content-type': 'test/html'} 
            conn.request('GET',request_url,headers = headers)  
            r= conn.getresponse()  
            #print r.status
            if r.status == 200:
                data = r.read()
                str1 = data.decode()
                dec = json.loads(str1)
                download(dec['imgs'], searchword)
            page += 60
        except Exception as e:
            print(e)
            page += 60
            continue
              
def download(data, searchword):
    for d in data:
        global imgCount
        imgCount += 1
        #url = d['thumbURL']
        #url = d['hoverURL']
        url = d['objURL']
        
        print(url)
        t = threading.Thread(target=downloadOne, args=(url, imgCount, searchword))
        t.setDaemon(True)
        t.start()

def downloadOne(url, index, searchword):
    global doneCount
    global ulist
    try:
        if url in ulist:
            doneCount = doneCount + 1
            return
        data = urlopen(url).read()
        pattern = re.compile(r'.*/(.*?)\.jpg',re.S)
        item = re.findall(pattern,url)
        FileName = searchword + '/' + searchword + '_img_' + str(index) +str('.jpg')
        print(FileName)
        if not os.path.exists(FileName):
            f = open(FileName,'wb')
            f.write(data)
            ulist.append(url)
    except:
        return

if  __name__ == '__main__':
    if len(sys.argv) == 1:
        exit(1);
    word = sys.argv[1]
    request(word)
