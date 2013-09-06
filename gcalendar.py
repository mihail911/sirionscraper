#!/usr/bin/python
import gflags
import httplib2
import json
import sirionreader

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS=gflags.FLAGS
accountname='blah blah'
FLOW=OAuth2WebServerFlow(client_id='629810497976.apps.googleusercontent.com',
						client_secret='bKe21DSz3q0C4jDbpoMhWobG',
						scope='https://www.googleapis.com/auth/calendar',
						user_agent='GoogleCalendarNotifier/Version1')

storage=Storage('calendar.dat')
credentials=storage.get()
if credentials is None or credentials.invalid==True:
	credentials=run(FLOW,storage)

http=httplib2.Http()
http=credentials.authorize(http)

service=build(serviceName='calendar',version='v3',
	http=http, developerKey='AIzaSyB7nDrkZIO_PJDXUh-GnioZnzG0p1H47JI')


def formGCalendarEvents():
	converteddatetimes=sirionreader.getConvertedTimes()
	for alltimes in converteddatetimes:
		key,value=alltimes.popitem()
		event={'summary': 'Sirion SEM Time', 'start':{'dateTime': key}, 'end': {
			'dateTime':value}}
		created_event=service.events().insert(calendarId=accountname, body=event).execute()

formGCalendarEvents()