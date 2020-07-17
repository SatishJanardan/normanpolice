import os, time, nltk, re, pprint, PyPDF4, requests

from django.db import models
from police.models import Filelist, Cat, Crime, OffenseCat, Officer, Arrest, Case
from datetime import datetime
import pytz

from django.shortcuts import render


filepath = 'cat details.csv'
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		(cName, cID, cSeverity, cUrgency) = line.split(",")
		if cnt != 1:
			#print(cName, cID, cSeverity, cUrgency)
			cat = Cat.objects.get(catId=cID)
			cat.catSeverity = cSeverity
			cat.catUrgency = cUrgency
			cat.save()
		
		line = fp.readline()
		cnt += 1


web_file=open('cat details.csv', 'r')

for csvline in web_file.readline(webfile):
#for line in csv_read.split('\n'):
	print("Line : {}".format(csvline.strip()))

web_file.close()