#!/usr/bin/python
import re
import urllib2
import pdb 

from bs4 import BeautifulSoup

monthtonumber={'January':'01', 'February':'02','March':'03', 'April':'04', 'May':'05', 'June':'06',
				'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11',
				'December':'12'}
scheduleurl='http://www.stanford.edu/group/snl/sem.htm'

def getScheduleURL():
	"""Gets URL where Sirion schedule is located."""
	startpage=urllib2.urlopen(scheduleurl)
	startpagesoup=BeautifulSoup(startpage)
	for tags in startpagesoup.find_all('a'):
		if tags.string=='SEM calendar':
			return tags['href']

def getExpandedPage(scheduleurl):
	"""Get expanded page URL."""
	expandedpage=urllib2.urlopen(scheduleurl)
	expandedpagesoup=BeautifulSoup(expandedpage)
	for imgurl in expandedpagesoup.find_all('a'):
		if imgurl.find('img') is not None:
			if imgurl.find('img').get('alt')== ' Expand ':
				return imgurl['href']

def getURLwithGivenString(soup,stringintags):
	"""Returns the value of 'href' associated with the tag that contains the given string--returns a list
	   with all such values."""
	allurls=[]
	for tag in soup.find_all('a'):
		if tag.string==stringintags:
			allurls.append(tag['href'])
	return allurls

def convertToSEMurlFormat(allurls):
	"""Converts given urls to appropriate SEM format."""
	conversionstring='http://snl.calendarhost.com/cgi-bin/calweb'
	for url in allurls:
		allurls[allurls.index(url)]=conversionstring+url[1:]

def getDateTime(givensoup):
	"""Gets the date and time info for a given soup."""
	datetimecontents=[]
	for contents in givensoup.find_all('td',valign='top'):
		if contents.renderContents().strip()=='Date/Time:':
			#pdb.set_trace()
			datetimeTD=contents.next_sibling.next_sibling.renderContents()
			datetimeTD=datetimeTD.split(', ')
			datetimecontents.extend([datetimeTD[1].split(' ')[0], datetimeTD[1].split(' ')[1],datetimeTD[3].split(' ')[0]])
	return datetimecontents

def getAllDateTime(myurls):
	"""For all urls given, find the date and time associated with that url and return as a 
	list as follows: ['Month', 'Day', 'StartTime']."""
	alldatetimes=[]
	for url in myurls:
		newpage=urllib2.urlopen(url).read()
		newsoup=BeautifulSoup(newpage)
		alldatetimes.append(getDateTime(newsoup))
	return alldatetimes

def convertTime(inputtime):
	indexcolon=inputtime.index(':')
	hour=int(inputtime[:indexcolon])
	ampm=inputtime[len(inputtime)-1]
	if ampm=='p':
		if hour!=12:
			hour+=12
	if ampm=='a' and hour==12:
		hour=str('00')
	minutes=inputtime[indexcolon:-1]
	return str(hour)+minutes

def convertToRFC(inputinfo):
	"""Converts a given date/time list to RFC 3339 standard time
	   input a list containing the date/time as returned above
	   set an end time 1 hour after start time
	   return as a dictionary--{start:end}.
	   This method was pretty lousily hard-coded."""
	startend={}
	start=[]
	end=[]
	monthnumber=monthtonumber[inputinfo[0]]
	convertedtime=convertTime(inputinfo[2])
	if int(inputinfo[1])<10:
		inputinfo[1]='0'+inputinfo[1]
	start.append('2013'+'-'+monthnumber+'-'+inputinfo[1]+'T'+convertedtime+':00.000-07:00')
	indexcolon=convertedtime.index(':')
	firstnum=int(convertedtime[:indexcolon])
	firstnum+=1
	endtime=''
	if firstnum<10:
		endtime='0'+str(firstnum)
	else:
		endtime=str(firstnum)
	end.append('2013'+'-'+monthnumber+'-'+inputinfo[1]+'T'+ endtime+':'+convertedtime[(indexcolon+1):]+':00.000-07:00')
	startend[start[0]]=end[0]
	return startend

def convertAllToRFC(alldatetimes):
	"""Convert the list of all date/time lists to RFC 339 format."""
	convertedtimes=[]
	for datetime in alldatetimes:
		convertedtimes.append(convertToRFC(datetime))
	return convertedtimes

def getConvertedTimes():
	"""Gets and returns all converted times from a parsing of the Sirion website page. 
	This function does all the heavy-lifting."""
	try:
		urlfrag=getExpandedPage(getScheduleURL())
		expandedpageurl='http://snl.calendarhost.com/cgi-bin/calweb'+urlfrag[1:]
		sempage=urllib2.urlopen(expandedpageurl)
		sempagesoup=BeautifulSoup(sempage)
	except:
		raise NameError('Could not open Sirion website')
	else:
		myurls=getURLwithGivenString(sempagesoup,'Mihail')
		convertToSEMurlFormat(myurls)
		alldatetimes=getAllDateTime(myurls)
		converted=convertAllToRFC(alldatetimes)
		return converted
