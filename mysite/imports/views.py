from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Count, Min, Sum
from plotly.offline import plot
import csv, io
import datetime as datatime
from django_pandas.io import read_frame
from django.contrib import messages
from datetime import datetime
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView,
	DeleteView
)

from police.models import Filelist,Graphdata, Cat, Crime, OffenseCat, Officer, Arrest, Case, Weather

def about(request):
	return render(request, 'imports/about.html', {'title': 'About'})


def csv_weather(request):  # Upload weather data from csv file.

	# declaring template
	template = "imports/csv_weather.html"
	data = Weather.objects.all()
	# prompt is a context variable that can have different values depending on their context
	prompt = {
		'order': 'Weather Data',
		'weather': data
			  }
	# GET request returns the value of the data with the specified key.
	if request.method == "GET":
		return render(request, template, prompt)
	csv_file = request.FILES['file']
	# let's check if it is a csv file
	if not csv_file.name.endswith('.csv'):
		messages.error(request, 'THIS IS NOT A CSV FILE')
	data_set = csv_file.read().decode('UTF-8')
	# setup a stream which is when we loop through each line we are able to handle a data in a stream
	io_string = io.StringIO(data_set)
	next(io_string)
	for column in csv.reader(io_string, delimiter=',', quotechar='"'):
		alist = Weather.objects.filter( wMonth = column[0], wDay = column[1] )  # Only add weather data it it did not exist before
		if (alist.count() == 0):
			_, created = Weather.objects.update_or_create(
				wMonth = column[0],
				wDay = column[1],
				wTempMax = column[2],
				wTempAvg = column[3],
				wTempMin = column[4],
				wDewMax = column[5],
				wDewAvg = column[6],
				wDewMin = column[7],
				wHumidityMax = column[8],
				wHumidityAvg = column[9],
				wHumidityMin = column[10],
				wWindMax = column[11],
				wWindAvg = column[12],
				wWindMin = column[13],
				wPressureMax = column[14],
				wPressureAvg = column[15],
				wPressureMin = column[16],
				wPrecipitation = column[17]
			)
		#print(io_string)
	context = {}
	return render(request, "imports/home.html", context)

def convert_pdf(filename):

	# Copy URL to local file copy for processing
	#r = requests.get(download_url, allow_redirects=True)
	#filename = download_url[download_url.rfind("/")+1:]  # Trim URL to get file name
	#open(filename, 'wb').write(r.content)  # Copy the file from web site to local disk
	#(prefix, sep, suffix) = filename.rpartition('.')
	
	web_file=open(filename, 'rb')
	read_pdf = PyPDF4.PdfFileReader(web_file)
	number_of_pages = read_pdf.getNumPages()
	headline=0


	filetype=1    # file type of incidents
	columnsext = 5			# numbr of columns of data to extract
	linerecord=["","","","",""]
	if filename.rfind("arrest") > 0:
		filetype=2  # file type of arrests
		linerecord=["","","","","","","","","","","",""]
		columnsext = 12

	if filename.rfind("case") > 0:
		filetype=3   # file type of case
	
	# Process each page to find just the incidents
	for pageNum in range(0, number_of_pages):
		
		page = read_pdf.getPage(pageNum)
		
		page_content = page.extractText()

		i=0
		fillfield=0
		

		for line_content in page_content.split('\n'):
			line_content = line_content.strip()  #Strip all extra charactors around line
			i+=1

			# Strip out the header line in the file
			if filetype == 1 and headline == 0:
				header = re.compile('^(?:Incident ORI)')
				if header.match(line_content):
					headline = 1
					linerecord=["","","","",""]
					fillfield=0
					i=0
					continue

			# Strip out the header line in the file
			if filetype == 2 and headline == 0:
				header = re.compile('^(?:Officer)')
				if header.match(line_content):
					headline = 1
					linerecord=["","","","","","","","","","","",""]
					fillfield=0
					i=0
					continue

			# Strip out the header line in the file
			if filetype == 3 and headline == 0:
				header = re.compile('^(?:Reporting Officer)')
				if header.match(line_content):
					headline = 1
					linerecord=["","","","",""]
					fillfield=0
					i=0
					continue

			# Strip out all lines that are short of all fields 
			if filetype == 1 and headline == 1:
				shortline = re.compile('^(?:OK[0-9][0-9][0-9][0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9][0-9]|EMSSTAT)$')
				#print(i,fillfield,line_content)
				if (i % columnsext > 0) and shortline.match(line_content):
					# print(i,fillfield,line_content,linerecord)
					linerecord=["","","","",""]
					fillfield=0
					i-=3
					continue

			if filetype == 2 and headline == 1:
				shortline = re.compile('^(?:[0-9][0-9][0-9][0-9] -)')
				if (i % columnsext > 0) and shortline.match(line_content):
					linerecord=["","","","","","","","","","","",""]
					i-=fillfield+1
					fillfield=0
					continue

			if filetype == 3 and headline == 1:
				shortline = re.compile('^(?:[0-9][0-9][0-9][0-9] -)')
				if (i % columnsext > 0) and shortline.match(line_content):
					# print(i,fillfield,line_content,linerecord)
					linerecord=["","","","",""]
					i-=fillfield+1
					fillfield=0
					continue
				shortline = re.compile('^(?:McDonough|Stonebreaker)$')
				if (i % columnsext > 0) and shortline.match(line_content):
					# print(i,fillfield,line_content,linerecord)
					linerecord=["","","","",""]
					i-=1
					fillfield=0
					continue

			# Process where data flows over multiple lines
			if i % columnsext == 0:	
				if filetype == 1:	# file type of incidents
					r = re.compile('^(?:OK[0-9][0-9][0-9][0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9][0-9]|EMSSTAT)$') 
					if r.match(line_content):
						j=0
					else:	# Swift all the field left by one; address spanding two lines
						linerecord[2]+=linerecord[3]
						linerecord[3]=linerecord[4]
						linerecord[4]=line_content
						fillfield-=1
						i-=1
				if filetype == 2:	# file type of arrests
					r = re.compile('^(?:[0-9][0-9][0-9][0-9] -)') 
					if r.match(line_content):
						j=0
					else:	# Swift all the field left by one; address spanding two lines
						case = re.compile('^(?:[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])') # Case number on second line
						if case.match(linerecord[2]):
							linerecord[1]+=linerecord[2]
							for j in range(2,columnsext-2):
								linerecord[j]=linerecord[j+1]
							linerecord[columnsext-1]=line_content
						else:
							linerecord[3]+=linerecord[4]
							for j in range(4,columnsext-2):
								linerecord[j]=linerecord[j+1]
							linerecord[columnsext-1]=line_content
						fillfield-=1
						i-=1
				if filetype == 3:	# file type of case
					r = re.compile('^(?:[0-9][0-9][0-9][0-9] -)') 
					if r.match(line_content):
						j=0
					else:	# Swift all the field left by one; address spanding two lines
						street = re.compile('^(?:STREET|AVE|ST|DR|BLVD|NE|LN|DRIVE)') 
						if street.match(line_content):		# Stree info on second line
							linerecord[2]+=linerecord[3]
							linerecord[3]=linerecord[4]
							linerecord[4]=line_content
						else:
							linerecord[3]+=linerecord[4]
							linerecord[4]=line_content
						fillfield-=1
						i-=1

			# Continue to process lines until end of is reached 
			if i % columnsext != 0:
				linerecord[fillfield]=line_content
				# print(linerecord,i,fillfield)
				fillfield += 1
			else:  # End of record reached - add recored to database
				linerecord[fillfield]=line_content
				# print(linerecord)

				# Add 
				if filetype == 1:
					cat = Cat.objects.filter(catName=linerecord[3])
					if cat.count() ==  0:
						cat = Cat( catName = linerecord[3].strip(),
									catSeverity = "L" )
						cat.save()
					cat = Cat.objects.get(catName=linerecord[3])

					crime = Crime( crimeDate = cstzone.localize(datetime.strptime(linerecord[0].strip(),"%m/%d/%Y %H:%M")),
									crimeNumber = linerecord[1].strip(),
									crimeLocation = linerecord[2].strip(),
									crimeCatId = cat,
									crimeORI = linerecord[4].strip() )

					#print(crime.crimeDate,crime.crimeNumber,crime.crimeLocation,crime.crimeCatId.catName,crime.crimeORI)
					crime.save()

				if filetype == 3:
					offenseCat = OffenseCat.objects.filter( offenseCat = linerecord[3] )
					if offenseCat.count() == 0:
						offenseCat = OffenseCat( offenseCat = linerecord[3].strip() )
						offenseCat.save()
					offenseCat = OffenseCat.objects.get( offenseCat = linerecord[3] )

					# print(linerecord[4])
					(badge, offname) = linerecord[4].split(' -')
					# badge = badge.strip()
					offname = offname.strip()
					officer = Officer.objects.filter( officerBadge = badge )
					if officer.count() == 0:
						officer = Officer( officerBadge = badge, officerName = offname )
						officer.save()
					officer = Officer.objects.get( officerBadge = badge )

					case = Case( caseDate = cstzone.localize(datetime.strptime(linerecord[0].strip(),"%m/%d/%Y %H:%M")),
									caseNumber = linerecord[1].strip(),
									caseLocation = linerecord[2].strip(),
									caseOffenseId= offenseCat,
									caseOfficerId = officer )
					#print(case.caseDate,case.caseNumber,case.caseLocation,case.caseOffenseId.offenseCat,case.caseOfficerId.officerBadge)
					case.save()

				# reset and get ready for next record
				if columnsext == 5:
					linerecord=["","","","",""]
				else:
					linerecord=["","","","","","","","","","","",""]
				fillfield=0
					
	filelist.save()  # record that this file has been processed completely
	web_file.close()
	
def pdf_norman(request):  # Upload files for norman police department.
	# declaring template
	template = "imports/home.html"
	data = Filelist.objects.all()
	# prompt is a context variable that can have different values depending on their context
	prompt = {
		'order': 'Norman Police Files',
		'weather': data
			  }
	# GET request returns the value of the data with the specified key.
	if request.method == "GET":
		return render(request, template, prompt)
	filename = request.FILES['file']
	# let's check if it is a csv file
	if not filename.name.endswith('.pdf'):
		raise ValidationError(_('THIS IS NOT A PDF FILE'))

	if filename.name.find('_incident_') == -1 or filename.name.find('_case_') == -1:
		raise ValidationError(_('NOT A FILE FROM NORMAN POLICE DEPT.'))

	# Only process the file if it has not been processed before
	filelist = Filelist.objects.filter( fileName = filename )
	if filelist.count() == 0:
		filelist = Filelist( fileName = filename )
		#messages.error(request, 'Processing URL')
		#print("Processing file",filename)
		convert_pdf(filename)
		messages.error(request, 'Done processing file')
		# record this file has been process after processing is complete.

	else:		#  Skip files that have been already processed
		web_file.close()
		raise ValidationError(_('THIS FILE HAS BEEN PROCESSED BEFORE'))

	#print(io_string)
	context = {}
	return render(request, "imports/home.html", context)

def update_gps(request):  # Upload weather data from csv file.

	# declaring template
	template = "imports/update_gps.html"
	data = Crime.objects.all()
	# prompt is a context variable that can have different values depending on their context
	prompt = {
		'order': 'GPS Data',
		'gpspoints': data
			  }
	# No input needed.

	#  Add add login to update all gps pointsin both crime and case tables

	context = {}
	return render(request, "imports/home.html", context)