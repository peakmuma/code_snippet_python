'''
用于校园网的自动登录
'''
import urllib.request
def atuoLogin(username,passwd):
	url='http://10.3.8.211'
	data='DDDDD={0}&upass={1}&0MKKey='.format(username,passwd)
	resp=urllib.request.urlopen(url,data.encode('utf-8'))
	resData=resp.read().decode('gb2312')
	if resData.find('Msg=02')>0:
		data='DDDDD={0}&upass={1}&passplace=&AMKKey='.format(username,passwd)
		urllib.request.urlopen(url+'/all.htm',data.encode('utf-8'))