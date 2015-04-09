import urllib.request
from bs4 import BeautifulSoup

external_url='http://gfw74.info/thread0806.php?fid=22&search=&page={0}'

def getUrl():
	for i in range(1):
		pageUrl=external_url.format(str(i+2))
		pageSoup=getSoup(pageUrl)
		if pageSoup is not None:
			trSoups=pageSoup.findAll('tr',class_='tr3 t_one')
			for trSoup in trSoups:
				processTrSoup(trSoup)

def processTrSoup(trSoup):
	tdSoups=trSoup.contents
	aSoup=tdSoups[1].find('h3').a
	commentNum=tdSoups[5].string
	print(aSoup.get('href'))
	print(str(aSoup.string,encoding='gbk'))
	print(commentNum)

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
