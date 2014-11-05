'''
这一段小代码是从金庸江湖网上下载金庸的小说，网址：http://www.jyjh.com.cn/jinyong/

参数说明：
path是文件路径
book是书的编号，类型是字符串，必须是两位数字
totalChapters是总章节数，本程序是分章节下载

使用示例：
getBook('e:\\书剑恩仇录.txt','08',22)

环境：python3.4,BeautifulSoup4,win 7
'''
from bs4 import BeautifulSoup
import urllib.request
import re
def getBook(path,book,totalChapters):
	with open(path,'w',encoding='gbk') as f:
		url='http://www.jyjh.com.cn/jinyong/{0}/mydoc{1}.htm'
		for i in range(1,totalChapters+1):
			chapter=str(i).zfill(3)
			resdata=urllib.request.urlopen(url.format(book,chapter)).read().decode('gbk','ignore')
			p=BeautifulSoup(resdata).findAll('p')#拿到所有的p元素
			title=p[0].getText()#章节名称在第一个p元素中
			content=p[1].getText()#章节内容在第二个p元素中
			pattern=re.compile(' {2,}')#章节内容的每段段首有好多空格，包括两个中文的空格\u3000
			content=pattern.sub('',content)#删除中文空格前面的空格
			f.write(title+'\n')
			f.write(content+'\n')
			print('book:%s chapter:%s success'%(book,chapter))
		print('book:%s success!!!'%(book))