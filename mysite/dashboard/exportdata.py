from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Count, Min, Sum
from plotly.offline import plot
import csv, io, datetime
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as datatime
from plotly.graph_objs import Scatter, Bar
from django_pandas.io import read_frame
from django.contrib import messages
import pytz, csv
import gmplot
from datetime import datetime
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView,
	DeleteView
)

from police.models import Cat, Crime, OffenseCat, Officer, Arrest, Case, Weather
from dashboard.forms import GraphTypeForm

cstzone=pytz.timezone("America/Chicago")  # Time zone of Norman, OK
bucketsize = 5 # minute facets
startdate=cstzone.localize(datetime.strptime("06/01/2020 00:00","%m/%d/%Y %H:%M"))
enddate=cstzone.localize(datetime.strptime("07/09/2020 12:00","%m/%d/%Y %H:%M"))
startsev=0
endsev=5

timelist = read_frame(Crime.objects.filter(
	crimeDate__range=(startdate,enddate),
	crimeCatId__catUrgency__gte=startsev,
	crimeCatId__catUrgency__lte=endsev).values('crimeDate',
			'crimeNumber','crimeLocation','crimeCatId__catName',
			'crimeCatId__catUrgency','crimeCatId__catSeverity',
			'crimeORI','crimeLat','crimeLong'
			))

'''
filename = "incidents.csv"
#import sys
sys.stdout = open(filename,'wt')
#csvfile = open(filename, 'w')
#for line in timelist['crimeCatId__catName']:
print('"crimeDate"','"crimeNumber"','"crimeLocation"','"crimeCatId__catName"',
			'"crimeCatId__catUrgency"','"crimeCatId__catSeverity"',
			'"crimeORI"','"crimeLat"','"crimeLong"')
timelist['crimeDate']
print(timelist['crimeDate'],timelist['crimeNumber'],timelist['crimeLocation'],
			timelist['crimeCatId__catName'],
			str(timelist['crimeCatId__catUrgency']),str(timelist['crimeCatId__catSeverity']),
			timelist['crimeORI'],str(timelist['crimeLat']),str(timelist['crimeLong'])
#csvfile.close()
close() '''

timelist.to_csv (r'incidents.csv', index = False, header=True, 
	quoting=csv.QUOTE_NONNUMERIC, columns=[
	'crimeDate','crimeNumber','crimeLocation','crimeCatId__catName',
			'crimeCatId__catUrgency','crimeCatId__catSeverity',
			'crimeORI','crimeLat','crimeLong'
	])



timelist = read_frame(Case.objects.filter(
	caseDate__range=(startdate,enddate)).values('caseDate',
		'caseNumber','caseOffenseId__offenseCat','caseOfficerId__officerBadge',
		'caseOfficerId__officerName','caseLat','caseLong'
		))

timelist.to_csv (r'cases.csv', index = False, quoting=csv.QUOTE_NONNUMERIC, 
	header=True, columns=['caseDate',
		'caseNumber','caseOffenseId__offenseCat','caseOfficerId__officerBadge',
		'caseOfficerId__officerName','caseLat','caseLong'
	])

close()