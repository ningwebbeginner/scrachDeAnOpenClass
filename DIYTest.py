import requests
from bs4 import BeautifulSoup
import bs4
import time
def getHTMLText(url):
	kv={'dept-select':"",
	'tbSearch': 'cis22c',
	'hfTerm': 'F2019'}
	try:
		r=requests.post(url,data=kv)
		r.raise_for_status()
		r.encoding= r.apparent_encoding
		return r.text
	except:
		return ""



def getClassInfo(lst,clURL):
	html=getHTMLText(clURL)
	soup=BeautifulSoup(html,"html.parser")
	css_soup=BeautifulSoup(html,"html.parser")
	for tr in soup.find_all('tbody'):
		if isinstance(tr,bs4.element.Tag):
			tds=tr('td')
			lst.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string])
	#for tr in css_soup.find_all(re.compile("d-CIS")):
		#tds=tr('td')
		#print(tds[0].string)

	print(lst)

def printClass(lst,num):
	print("{:^5}\t{:^10}".format("CRN","seats"))
	for i in range(num):
		l=lst[i]
		print("{:^5}\t{:^10}\t{:^10}\t{:^10}".format(l[0],l[1],l[2],l[3]))
		

def main():
	classUrl='https://www.deanza.edu/schedule/listings.html'
	output_file='E://classTnfo.txt'
	while True:
		clist=[]
		num=1
		getClassInfo(clist,classUrl)
		printClass(clist,num)
		l=clist[0]
		
		if (l[3]!="Full"):
			print(l[0])
			print(time.ctime())
			break
		time.sleep(60)

main()

