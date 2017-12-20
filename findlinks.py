# -*- coding:utf-8 -*-
# Author: Muhe
# Version:2.0
# 不爬相似地址了。
# 有时候xml解析会报错

from __future__ import division
import lxml
from lxml.html import fromstring
import requests
import re
import mechanize
import operator
import sys
import os
from time import sleep

class SameFileError(Exception): pass
class NoneTypeError(Exception): pass


global formlist
reqlist = []
feature_hub = []
_Root = os.getcwd()

# 请求一个链接，返回HTTP类型、主机Host名、页面的二进制数据
def _requestData(url):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        # 'Cookie': '',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        req = requests.get(url, headers=headers,timeout=5)
    except:
        return 'err ', url, None
    return req.status_code, url, req.text


def getLinks(self):
    try:
        resType, resHost, resData = _requestData(self)
        if not resData:
            raise NoneTypeError
        doc = lxml.html.document_fromstring(resData)
        tags = ['a', 'iframe', 'frame']
        doc.make_links_absolute(resHost)
    except Exception,NoneTypeError:
        return resHost, None
    links = doc.iterlinks()
    trueLinks = []
    for l in links:
        if l[0].tag in tags:
            trueLinks.append(l[2])
    return trueLinks, resData  # 要确保是绝对路径


def correct_url(url):
    if 'http://' not in url:
        url = 'http://' + url.strip()
    return url


def middle_name(url):
    # middle_name = re.findall(r'[\/\.]([\s\S]+)\.', url)
    # tidy the url
    url_tidy = url.strip('www.')
    url_tidy = url_tidy.strip('http://')
    url_tidy = url_tidy.strip('https://')
    # dot = re.findall('\.', url_tidy)
    re_url = re.compile(r'([-\w]+).')
    try:
        middle = re_url.match(url_tidy).groups(0)
    except Exception:
        return None
    return middle[0]

def getdiffer(list1,list2):
    if len(list1)<len(list2):
        length = len(list1)
        if (len(list2)-len(list1))>5:
            return False
    else:
        length = len(list2)
        if (len(list1)-len(list2))>5:
            return False
    return length

def str_compare(str1,str2,accuracy=0.80):
    list1 = list(str1)
    list2 = list(str2)
    score = 0
    # print "comparing:",str1,str2
    total = len(list1)
    length = getdiffer(list1,list2)
    if length is False:return False
    for i in xrange(length):
        if list1[i] == list2[i]:
            score += 1
    ratio = score/total
    if ratio > accuracy:
        # print "similier"
        return True
    return False


def feature_match(link):
	global url_old
	for link_old in url_old:
		if str_compare(link_old,link):
			return True
	return False


def feature_catch(link):
    pass


def feature_filter(link):
    # 检测是否匹配已有特征
    if feature_match(link):
        return True
    return False


def single_url(url):
# 获取单一url入口
    # try:
    global url_ad
    global url_old
    global middle
    url = correct_url(url)
    # 获取页面上链接、数据
    url_links, data = getLinks(url)
    if data is None:
        return
    for link in url_links:
        sys.stdout.write('!')
        if link == url:
            continue
        if link in url + '/index':
            continue
        if 'javascript' in link:
            continue
        if link in url_old:
            continue
        if middle not in link:
            continue
        if feature_filter(link):
            continue
        try:
            print "\n",link
        except Exception:
            pass
        with open(_Root + "\\Results\\" + middle + "_links.txt","a") as f:
            print "writing: ",link
            f.write(link+"\n")
        # if link not in url_old and link not in url_add and 'http://www.xxx.com' in link:
        # print link
        # Findsubmit(link)
        url_add.append(link)
        url_old.append(link)  # 因为已经加入到add，所以算是已知url，就加入old里。
        # except Exception, e:
        #     print e
        #     pass


def Findsubmit(link):
    global reqlist
    try:
        br = mechanize.Browser()  # initiating the browser
        br._factory.is_html = True
        br.addheaders = [('User-agent',
                          'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open(str(link), timeout=15)
        if br.forms():
            params = list(br.forms())
            for par in params:
                for p in par.controls:
                    ps = str(p)
                    # print p.name
                    if 'TextControl' in ps:
                        param = str(p.name)
                        reqstr = par.action + par.method + param
                        if reqstr not in reqlist:
                            reqlist.append(reqstr)
                            testxss(par.action, par.method, param)
    except Exception, e:
        print e
        pass


def testxss(action, method, param):
    method = method.lower()
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    if method == "get":
        print "=" * 10 + "get start" + "=" * 10
        url = action + "/?" + param + "=test1234"
        print url
        # response = requests.get(url,headers=headers)
        # print response.text
        print "=" * 10 + "get end" + "=" * 10
    if method == "post":
        data = {'{0}'.format(param): "test"}
        print "=" * 10 + "post start" + "=" * 10
        print action
        print data
        # response = requests.post(action,data=data,headers=headers)
        # print response.text
        print "=" * 10 + "post end" + "=" * 10


def findlink(input,level=2):
    global url_new
    global url_old
    global url_add
    global middle
    # 总入口
    url_new = []  # level_i级的
    url_old = []  # 所有已经爬过的
    url_add = []  # 每个level_i级新增的链接
    # url = 'http://www.xxx.com'
    url = input
    middle = middle_name(url)
    url_new.append(url)
    for level_i in xrange(level):
        for i in xrange(len(url_new)):
            url_new_i = url_new[i]
            url_old.append(url_new_i)
            sleep(0.5)
            single_url(url_new_i)
        url_new = url_add
    # with open(middle + "_links.txt","w") as f:
        # for line in url_old:
            # f.write(line+"\n")


if __name__ == '__main__':
    try:
        url=sys.argv[1]
    except Exception:
        print "Usage: python findlinks.py www.example.com"
        exit()
    # url = 'http://www.xxx.com'
    findlink(url,10)