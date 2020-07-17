import os, time, nltk, re, pprint, PyPDF4, requests, csv, io

from django.db import models
from police.models import Filelist, Cat, Crime, OffenseCat, Officer, Arrest, Case, Weather
from datetime import datetime
import pytz

from django.shortcuts import render
from django.contrib import messages

# Create your views here.
# one parameter named request
def csv_upload(request):
    # declaring template
    template = "profile_upload.html"
    data = Profile.objects.all()
	# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'profiles': data    
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
	for column in csv.reader(io_string, delimiter=',', quotechar="|"):
	    _, created = Profile.objects.update_or_create(
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
	context = {}
	return render(request, template, context)