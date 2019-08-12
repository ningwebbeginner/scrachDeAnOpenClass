import requests
from bs4 import BeautifulSoup
import bs4
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
def getHTMLText(url):
	kv={'dept-select':"",
	'tbSearch': 'cis22C',
	'hfTerm': 'F2019'}#  from data in the header 
	try:
		r=requests.post(url,data=kv)
		r.raise_for_status()
		r.encoding= r.apparent_encoding
		return r.text
	except:
		return ""



def getClassInfo(lst,clURL,lnum):
	while True:
		html=getHTMLText(clURL)
		if (html!=""):
			break
	soup=BeautifulSoup(html,"html.parser")
	#css_soup=BeautifulSoup(html,"html.parser")
	for tr in soup.find_all('tbody'):
		if isinstance(tr,bs4.element.Tag):
			table_rows=tr.find_all('tr')
			for trs in table_rows:
				#td=trs.find_all('td')
				#print(td)
				tds=trs.find_all('td')
				if (tds[0].string!="LAB"):
					lst.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string])
					lnum+=1
	#for tr in css_soup.find_all(re.compile("d-CIS")):
		#tds=tr('td')
		#print(tds[0].string)

	#print(lst)
	#print(lnum)

def printClass(lst,num):
	#print("{:^5}\t{:^10}".format("CRN","seats"))
	for i in range(num):
		l=lst[i]
		print("{:^5}\t{:^10}\t{:^10}\t{:^10}".format(l[0],l[1],l[2],l[3]))

def sendGmailtoYahoo(lMessage):
	from_address = ""
	to_address = ""
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Test email"
	msg['From'] = from_address
	msg['To'] = to_address
	# Create the message (HTML).
	html = lMessage[0]+','+lMessage[1]+','+lMessage[3]+','+time.ctime()
	# Record the MIME type - text/html.
	part1 = MIMEText(html, 'html')
	# Attach parts into message container
	msg.attach(part1)
	# Credentials
	username = ''  
	password = ''  
	# Sending the email
	## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
	server = smtplib.SMTP('smtp.gmail.com', 587) 
	server.ehlo()
	server.starttls()
	server.login(username,password)  
	server.sendmail(from_address, to_address, msg.as_string())  
	server.quit()

def main():
	classUrl='https://www.deanza.edu/schedule/listings.html'
	output_file='E://classTnfo.txt'
	count=0
	while True:
		clist=[]
		num=1# the number of the course in index
		getClassInfo(clist,classUrl,num)
		#printClass(clist,num)
		l=clist[num-1]
		count+=1
		#if (count==10):
			#sys.stdout.flush()
			#print(count)
			#count=0
		if (l[3]!="Full"):
			sendGmailtoYahoo(l)
			#file1 = open("Aptint.txt","a")#append mode 
			#file1.write(l[0]+','+l[1]+','+l[3]+','+time.ctime()+'\n') 
			#file1.close()
			break
		time.sleep(5)


main()

