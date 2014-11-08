import re
import time
import calendar
import urllib.request
from socket import timeout
from bs4 import BeautifulSoup

external_url='http://www.patent-cn.com/{0}/{1}/{2}'
pattern=re.compile('\d+')
dayUrlList=[]
postUrlList=[]

def getUrls(year,month):	
	page=BeautifulSoup('<html><head></head><body><ul></ul></body></html>')
	litags=BeautifulSoup()
	days=calendar.monthrange(year,month)[1]
	for i in range(1,days+1):
		dayUrl=external_url.format(str(year),str(month).zfill(2),str(i).zfill(2))
		processDayUrl(dayUrl,litags,True)
		print('第 %d 天搜索完成'%(i))
	global dayUrlList
	global postUrlList
	for dayUrl in dayUrlList:
		processDayUrl(url,litags,False)
	for postUrl in postUrlList:
		processPostUrl(postUrl,litags,False)
	print('超时内容搜索完成')
	dayUrlList=[]
	postUrlList=[]
	path='e:\\patent-cn.html'
	with open(path,'w') as f:
		f.write(page.prettify())

def processDayUrl(url,litags,reProcess):
	while True:
		soup=getSoup(url,'day',reProcess)
		if soup is not None:
			posts=soup.findAll(attrs={'class':'post'})					
			for post in posts:
				postUrl=post.a.get('href')
				processPostUrl(postUrl,litags,True)
			next=soup.find('div',class_='navigation').find('div',class_='alignleft').a
			if next is not None:
				url=next.get('href')
			else:
				break
		else:
			break

def processPostUrl(url,litags,reProcess):
	soup=getSoup(url,'post',reProcess)
	if soup is not None:
		titleText=soup.find('li',class_='topic').a.getText()
		rateText=soup.find('div',class_='post-ratings').getText()
		print('内容：%s,评分：%s'%(titleText,rateText))
		scores=pattern.findall(rateText)
		if len(scores)>2:
			count=int(scores[0])
			grade=int(scores[1])
			if (count<10 and grade>=9) or (count>=10 and grade>=8):
				litag=BeautifulSoup('<li></li>')
				atag=litag.new_tag('a',href=url)
				atag.string=titleText
				litag.li.append(atag)
				litag.li.append(rateText)
				litags.append(litag)

def getSoup(url,type,reProcess):
	reConTimes=3
	if type=='day':
		TIMEOUT=10
	else:
		TIMEOUT=5
	while reConTimes>0:
		try:			
			with urllib.request.urlopen(url,timeout=TIMEOUT) as res:
				return BeautifulSoup(res.read().decode('utf-8','ignore'))			
		except timeout:
			reConTimes-=1			
		except Exception as e:
			print('url：%s不成功'%(url))
			break
	if reConTimes==0:
		if reProcess:
			global dayUrlList
			global postUrlList
			if type=='day':
				dayUrlList.append(url)
			else:
				postUrlList.append(url)
		else:
			print('url：%s超时'%(url))
	return None

def htmlProcess():
	litag=BeautifulSoup('<li></li>')
	atag=litag.new_tag('a',href=url)
	atag.string=titleText
	litag.li.append(atag)
	litag.li.append(rateText)
	litags.append(litag)
	with open(path,'w') as f:
		f.write(page.prettify())