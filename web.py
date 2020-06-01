#coding:utf-8
import urllib.parse
import urllib.request
import requests
import time 
import os
from pathlib import Path

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 

# 去除重复
def unique(row):
    result = []
    for i in row:
        if i not in result:
            result.append(i)
    return result
# 获取html文档
def getHtml(url):
    # 定制请求头User-Agent,火狐
    req = urllib.request.Request(url = url, headers = headers)  
    doctype = urllib.request.urlopen(req).read()   
    try:      
        doctype = doctype.decode('utf-8')
    except Exception as e:
        doctype = doctype.decode('gbk')
    return doctype
# 查找出html中标签 
def getHtmlTag(html,tag):   
    h = '<' + tag + ' '       
    noClose = ['br','hr','img','input','link','meta','area','base','col','command','embed','param','source','track','wbr']     
    if tag in noClose:
        c = '>'
    else:
        c = '</' + tag + '>'
    post = -len(h)
    posc = -len(c)
    list = []
    i = 0    
    htmlStr = str(html)
    while i < htmlStr.count('<' + tag + ' '):
        post = htmlStr.find(h,post + len(h))
        posc = htmlStr.find(c,post + len(h))
        tagHtml = htmlStr[post : posc + len(c)]      
        list.append(tagHtml)   
        i += 1
    return list
# 获取标签中属性
def getTagAtt(tag,att):
    s = ' ' + att + '="'
    e = '"'
    val = ''
    poss = tag.find(s)
    if poss != -1:
        pose = tag.find(e,poss + len(s))
        if pose != -1:
            val = tag[poss + len(s) : pose + len(e)-1] 
    return val  
# 设置标签中属性
def setTagAtt(tag,att,val):
    s = ' ' + att + '="'
    e = '"'
    if tag.find(s) == -1:
        attA = s + val + e
        str1 = tag[:tag.find('>')]
        str2 = tag[tag.find('>'):]
        tag = str1 + s + val + e + str2
    else:    
        poss = tag.find(s)
        pose = tag.find(e,poss + len(s))
        attB = tag[poss : pose + 1]
        attA = s + val + e
        tag = tag.replace(attB,attA)
    return tag
# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    list = []
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        list.append(child)
    return list
# 图片路径转成后缀 
def imgurl_TO_suffix(url):
    urlparse = urllib.parse.urlparse(url)        
    imgSuffixList = ['bmp','jpg','png','tif','gif','pcx','tga','exif','fpx','svg','psd','cdr','pcd','dxf','ufo','eps','ai','raw','WMF','webp']     
    urlFilePath = urlparse.path[urlparse.path.rfind('/')+len('/'):]
    suffix = urlFilePath[urlFilePath.rfind('.')+len('.'):]
    if suffix not in imgSuffixList:
        suffix = 'jpg'
    return suffix
def getDomainName(url):
    urlparse = urllib.parse.urlparse(url)
    domainName = urlparse.scheme + '://' + urlparse.netloc 
    return domainName
# 下载文件
def downloadFile(url,path = ''):       
    urlparse = urllib.parse.urlparse(url)
    urlPath = urlparse.path
    urlPath = urlPath[urlPath.rfind('/') + 1:]
    
    if urlPath.find('.css') >= 0 :
        if path != '':
            fileName = 'css/' + path 
        else:
            fileName = 'css/' + urlPath.replace('/','_') 
        if Path(fileName).is_file() == False:
            try:        
                urllib.request.urlretrieve(url, fileName)
            except Exception as e:
                print(e)           
    elif urlPath.find('.js') >= 0 :
        if path != '':
            fileName = 'js/' + path 
        else:
            fileName = 'js/' + urlPath.replace('/','_') 
        if Path(fileName).is_file() == False:
            try:        
                urllib.request.urlretrieve(url, fileName)
            except Exception as e:
                print(e)   
    else:
        fileName = urlPath[:urlPath.find('.')]
        if path.find('.') != -1:
            fileName = 'images/' + path[:path.find('.')] + "." + imgurl_TO_suffix(url) 
        else:
            fileName = 'images/' + fileName + "." + imgurl_TO_suffix(url) 


        if Path(fileName).is_file() == False:            
            try:
                response = requests.get(url, timeout=10, headers = headers)  
                time.sleep(2)
            except requests.exceptions.ConnectionError:
                print('【错误】当前图片无法下载')
            fp = open(fileName, 'wb')
            fp.write(response.content)
            fp.close()   
    return fileName
def hrefVali(href,domainName):    
    if href.count('//') == 0:
        href = domainName + href
    elif href.count('//') == 1:      
        if href.count('://') != 1:     
            href = 'http:' + href  
    return href
def url_input(label,error):
    while True:
        url = input('链接：')
        urlparse = urllib.parse.urlparse(url)
        if urlparse.netloc == '':
            print(error)
            continue
        break
    return  url    

def getTextResources(text,url,type=1):
    h = 'url('    
    c = ')'
    post = -len(h)
    posc = -len(c)
    list = []
    old = []
    i = 0    
    text = str(text)
    while i < text.count(h):
        post = text.find(h,post + len(h))
        posc = text.find(c,post + len(h))
        path = text[post + len(h): posc]      
        path = path.replace("'",'"')
        path = path.replace('"','') 
        
        path1 = url[:url.rfind('/')]
        path2 = url[:path1.rfind('/')]
        if path.find('../') != -1:
            filePath = path2 + '/' + path.replace('../','')
        else:
            filePath = path1 + '/' + path
        if filePath not in list:
            list.append(filePath)
            old.append(path)
        i += 1   
    if type == 0:
        return [list,old] 
    elif type == 1:
        return list          
def getResources(url):
    list = []  
    text =  getHtml(url)
    resourcesList = getTextResources(text,url)   
    for i in resourcesList:    
        if i not in list:
            list.append(i) 
    return list

def saveTowFile(url):
    pathName =  urllib.parse.urlparse(url).path[1:].replace('/','_')
    if url.find('.css') != -1:
        pathName = "css/" + pathName
        cssDoc = getHtml(url)   
        data = getTextResources(cssDoc,url,type=0)
        i = 0
        for i in range(len(data[0])):        
            str1 =  urllib.parse.urlparse(data[0][i]).path[1:].replace('/','_')
            if data[0][i].find('.css') != -1:
                cssDoc = cssDoc.replace(data[1][i],"" + str1)
            else:
                cssDoc = cssDoc.replace(data[1][i],"../images/" + str1)
        try:      
            fp = open(pathName,'w',encoding='utf-8')                            
            fp.write(cssDoc)        
            fp.close()
        except Exception as e: 
            print(e) 
    else:    
        downloadFile(url,pathName)    

def getTowFileUrl(url):
    cssList = []   
    cssList.append(url)  
    imgList = []  
    list1 = getResources(url)
    for i in list1:
        if i.find('.css') != -1:
            cssList.append(i)  
            list2 = getResources(i)
            for o in list2:
                if o.find('.css') != -1:
                    cssList.append(o)   
                    list3 = getResources(o)    
                    for s in list3:
                        if s.find('.css') != -1:
                            cssList.append(s)             
                        else:
                            imgList.append(s)            
                else:
                    imgList.append(o)                  
        else:
            imgList.append(i) 
    return cssList + imgList

print('--------请输入链接--------')
label = '链接：'
error = '--------链接格式错误，请重新输入--------'
url = url_input(label,error)

domainName = getDomainName(url)

html = getHtml(url)
cssList = getHtmlTag(html,'link')   
scriptList = getHtmlTag(html,'script')
imgList = getHtmlTag(html,'img')

cssPath = 'css'
jsPath = 'js'
imgPath = 'images'
if Path(cssPath).is_dir() == False:
    os.mkdir(cssPath) 
if Path(jsPath).is_dir() == False:
    os.mkdir(jsPath) 
if Path(imgPath).is_dir() == False:
    os.mkdir(imgPath) 

for i in cssList:    
    tag = i.replace("'",'"')
    cssHref = getTagAtt(tag,'href')    
    if cssHref.find('.css') != -1:

        towData = getTowFileUrl(cssHref)
        for qs in towData:
            saveTowFile(qs)        
        path =  urllib.parse.urlparse(cssHref).path[1:].replace('/','_')
        newTag = setTagAtt(tag,'href','css/'+ path)   
        html = html.replace(i,newTag)

for i in scriptList:
    tag = i.replace("'",'"')
    jsSrc = getTagAtt(tag,'src')
    if jsSrc != '':
        jsSrc = hrefVali(jsSrc,domainName)
        path = downloadFile(jsSrc)
        newTag = setTagAtt(tag,'src',path)    
        html = html.replace(i,newTag)
for i in imgList:  
    tag = i.replace("'",'"')
    imgSrc = getTagAtt(tag,'src')
    if imgSrc != '':
        imgSrc = hrefVali(imgSrc,domainName)
        path = downloadFile(imgSrc)
        newTag = setTagAtt(tag,'src',path)    
        html = html.replace(i,newTag)
try:      
    path = 'index.html'
    fp = open(path,'w',encoding='utf-8')
    fp.write(html)        
    fp.close()
except Exception as e:
    print(e) 

input('执行完成')

