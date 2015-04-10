import urllib.request
from bs4 import BeautifulSoup
from operator import itemgetter

external_url='http://gfw74.info/thread0806.php?fid=22&search=&page={0}'
external_list=[]

def getUrl():
	for i in range(8):
		pageUrl=external_url.format(str(i+2))
		pageSoup=getSoup(pageUrl)
		if pageSoup is not None:
			trSoups=pageSoup.findAll('tr',class_='tr3 t_one')
			for trSoup in trSoups:
				processTrSoup(trSoup)
	global external_list
	external_list=sorted(external_list,key=itemgetter('commentNum'),reverse=True)
	print(external_list[:10])

def processTrSoup(trSoup):
	tdSoups=trSoup.contents
	aSoup=tdSoups[1].find('h3').a
	commentNum=tdSoups[5].string
	oneRecord={'url':aSoup.get('href'),'title':aSoup.string,'commentNum':int(commentNum)}
	global external_list
	external_list.append(oneRecord)

def getSoup(url,reConTimes=3):
	for i in range(reConTimes):#todo,need i?
		try:			
			with urllib.request.urlopen(url,timeout=5) as res:
				return BeautifulSoup(res.read().decode('gb2312','ignore'))						
		except Exception as e:
			pass
	path='e:\\gfw74\\unSucessUrlList.txt'
	with open(path,'a') as f:
		f.write(url+'\n')
	return None
