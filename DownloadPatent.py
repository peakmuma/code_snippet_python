import re
import os
import calendar
import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter

external_url='http://www.patent-cn.com/{0}/{1}/{2}'
pattern=re.compile('\d+')
monthPatents=[]
dayTimeOutURLs=[]
patentTimeOutURLs=[]

def getAYearPatent(year):
	for i in range(12):
		getAMonthPatent(year,i+1)

def getAMonthPatent(year,month):
	global monthPatents
	date=str(year)+'.'+str(month).zfill(2)
	monthPatents.append(str({'type':'date','date':date}))#eval(string)转换成字典
	days=calendar.monthrange(year,month)[1]
	for i in range(days):
		dayUrl=external_url.format(str(year),str(month).zfill(2),str(i+1).zfill(2))
		processDayUrl(dayUrl,True)
		print('第 %d 天搜索完成'%(i+1))
	processTimeOutURLs()
	path='e:\\patent\\patent-cn-{0}.txt'.format(str(year))	
	with open(path,'a') as f:
		f.write('\n'.join(monthPatents))
		f.write('\n')
	monthPatents=[]
	print('第 %d 个月搜索完成'%(month))

def processTimeOutURLs():
	global dayTimeOutURLs
	global patentTimeOutURLs
	for dayUrl in dayTimeOutURLs:
		processDayUrl(dayUrl,False)
	for patentUrl in patentTimeOutURLs:
		processPatentUrl(patentUrl,False)	
	dayTimeOutURLs=[]
	patentTimeOutURLs=[]
	print('超时内容搜索完成')

def processDayUrl(url,reProcess):
	while True:
		soup=getSoup(url,'day',reProcess)
		if soup is not None:
			posts=soup.findAll('div',class_='post')				
			for post in posts:
				patentUrl=post.a.get('href')
				processPatentUrl(patentUrl,True)
			next=soup.find('div',class_='navigation').find('div',class_='alignleft').a
			if next is not None:
				url=next.get('href')
			else:
				break
		else:
			break

def processPatentUrl(url,reProcess):
	soup=getSoup(url,'post',reProcess)
	if soup is not None:
		titleText=soup.find('li',class_='topic').a.getText()
		rateText=soup.find('div',class_='post-ratings').getText()
		#print('内容：%s,评分：%s'%(titleText,rateText))
		scores=pattern.findall(rateText)
		if len(scores)>2:
			count=int(scores[0])
			grade=int(scores[1])
			if (count<10 and grade>=9) or (count>=10 and grade>=8):
				patent={'type':'patent','title':titleText,'rate':rateText,'url':url}
				global monthPatents
				monthPatents.append(str(patent))

def getSoup(url,type,reProcess,reConTimes=3):
	if type=='day':
		TIMEOUT=10
	else:
		TIMEOUT=5
	for i in range(reConTimes):#todo,need i?
		try:			
			with urllib.request.urlopen(url,timeout=TIMEOUT) as res:
				return BeautifulSoup(res.read().decode('utf-8','ignore'))						
		except Exception as e:
			pass
	if reProcess:
		global dayTimeOutURLs
		global patentTimeOutURLs
		if type=='day':
			dayTimeOutURLs.append(url)
		else:
			patentTimeOutURLs.append(url)
	else:
		path='e:\\patent\\unSucessUrlList.txt'
		with open(path,'a') as f:
			f.write(url+'\n')
	return None

def buildHtml(year):
	dataFilePath='e:\\patent\\patent-cn-{0}.txt'.format(str(year))
	if os.path.exists(dataFilePath):
		htmlFilePath='e:\\patent\\patent-cn-{0}.html'.format(str(year))
		soup=BeautifulSoup('<html><head></head><body><ul></ul></body></html>')
		ul=soup.ul
		patents=[]
		with open(dataFilePath,'r') as f:
			for each_line in f:
				patent=eval(each_line)
				if patent['type']=='patent':
					rate=pattern.findall(patent['rate'])
					if int(rate[1])>=9:
						patent['count']=int(rate[0])
						patents.append(patent)
		patents=sorted(patents,key=itemgetter('count'),reverse=True)
		soup=BeautifulSoup('<html><head></head><body><ul></ul></body></html>')
		ul=soup.ul
		for patent in patents[0:20]:
			li=soup.new_tag('li')
			a=soup.new_tag('a',href=patent['url'],target='_blank')
			a.string=patent['title']
			li.append(a)
			li.append(patent['rate'])
			ul.append(li)
		with open(htmlFilePath,'w') as f:			
			f.write(soup.prettify())





