import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter

external_url='http://gfw74.info/thread0806.php?fid=22&search=&page={0}'
external_list=[]

def getUrl(page):
	for i in range(page):
		pageUrl=external_url.format(str(i+2))
		pageSoup=getSoup(pageUrl)
		if pageSoup is not None:
			trSoups=pageSoup.findAll('tr',class_='tr3 t_one')
			for trSoup in trSoups:
				processTrSoup(trSoup)
				print('第%d页搜索完成'%(i+2))
	global external_list
	datalist=duplicate(external_list)
	datalist=sorted(datalist,key=itemgetter('maxCommentNum'),reverse=True)
	for i in range(10)
		print(datalist[i])
	path='home/peakmuma/code/python/successful/gfw74.html'
	buildHtml(datalist,path)

def processTrSoup(trSoup):
	tdSoups=trSoup.contents
	aSoup=tdSoups[1].find('h3').a
	commentNum=tdSoups[5].string
	oneRecord={'url':aSoup.get('href'),'title':aSoup.string,'maxCommentNum':int(commentNum),'commentNums':[int(commentNum)]}
	global external_list
	external_list.append(oneRecord)

def getSoup(url,reConTimes=5):
	for i in range(reConTimes):#todo,need i?
		try:			
			with urllib.request.urlopen(url,timeout=7) as res:
				return BeautifulSoup(res.read().decode('gb2312','ignore'))						
		except Exception as e:
			pass
	path='/home/peakmuma/code/python/unSuccessfulUrl/gfw74'
	with open(path,'a') as f:
		f.write(url+'\n')
	return None

def duplicate(datalist):
	datalist=sorted(datalist,key=itemgetter('title'))
	dataListLength=1
	for i in range(1,len(datalist)):
		if datalist[i]['title'] == datalist[dataListLength-1]['title']:
			datalist[dataListLength-1]['commentNums'].append(datalist[i]['commentNums'][0])
		else:
			datalist[dataListLength-1]['maxCommentNum'] = max(datalist[dataListLength-1]['commentNums'])
			dataListLength=dataListLength+1
	return datalist[0:dataListLength]

def buildHtml(dataList,path,start=0,end=100):
	soup=BeautifulSoup('<html><head></head><body><ul></ul></body></html>')
	ul=soup.ul
	for data in dataList[start:end]:
		data['url']='http://gfw74.info/'+data['url']
		li=soup.new_tag('li')
		a=soup.new_tag('a',href=data['url'],target='_blank')
		a.string=data['title']
		li.append(a)
		li.append(data['commentNum'])
		ul.append(li)
	with open(path,'w') as f:			
		f.write(soup.prettify())