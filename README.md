sirionscraper
=============


***Background***

This program was born out of my attempt to combat my absent-mindedness during my summer research internship in the electrical engineering department. Here's the backstory: my research this summer entailed that I spend a certain number of hours basically every week operating a scanning electron microscope known as the Sirion SEM. This device is in high demand among all departments on campus, so the nanofabrication center created a website application whereby people could sign up and reserve time slots for personal use of the machine. Because Sirion was so widely needed, I typically had to make reservations at least 1.5 weeks in advance of when I actually planned to use the machine. Thus naturally, when the day of my reservation actually rolled around, I had long forgotten that I had ever reserved a slot. This led to more than a fair number od "D'oh" moments where I would remember at night that I had missed a reservation several hours ago. 

In an effort to alleviate this problem (and also to get some practice parsing HTML pages with BeautifulSoup), I decided to make this program. The somewhat contrived solution I came up with was to write a program that would parse the Sirion SEM web page, finding the slots I had reserved. Using the API's provided for Google services, the program then updates my Google calendar, setting a reminder for the time slots. Given that I had configured my Google calendar to send text message reminders to my phone prior to any scheduled event, this would at least give me a 15 minute heads-up that I had a Sirion reservation waiting for me. I also created a cronjob that ran the entire program every Sunday night as a daemon process, so that I wouldn't run into the ironic problem of forgetting to run the program that was supposed to help me stop forgetting when my reservations were. 

All in all, it's a short little program that certainly worked as it was supposed to and gave me a chance to mess around with BeautifulSoup a bit. 

============================

***Use***

Though the program is pretty domain specific (i.e. I don't imagine most people need to scrape date/time information off the Sirion SEM website), I'll include some basic usage instructions.

Save the ```gcalendar.py``` and ```sirionreader.py``` files in the same directory. Update the ```accountname``` variable in ```gcalendar.py``` with the name of the Google account you wish to use. Run ```gcalendar.py```. 
You will probably be required to authorize your Google account the first time manually, but afterwards the program should be able to use the refresh access token included in the calendar.dat file that will in the directory where the .py files were saved. That's it! Your Google calendar should be updated!
