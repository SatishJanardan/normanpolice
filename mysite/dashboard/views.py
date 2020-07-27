from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
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
import pytz
import gmplot
from datetime import datetime
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView,
	DeleteView
)

from police.models import Graphdata, Cat, Crime, OffenseCat, Officer, Arrest, Case, Weather
from dashboard.forms import GraphTypeForm

# Create your views here.
def CountFrequency(my_list): 
  
	# Creating an empty dictionary  
	freq = {} 
	for item in my_list: 
		if (item in freq): 
			freq[item] += 1
		else: 
			freq[item] = 1
  
	return freq

def GraphAView(startdate,enddate,starturg,endurg,bucketsize):
	
	title = 'Graph A: Incidents Frequency (in ' + str(bucketsize) +' minute facets)'
	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeDate').order_by())

	timelisttemp = sorted(round((pd.to_datetime(timelist['crimeDate']).dt.hour*60+pd.to_datetime(timelist['crimeDate']).dt.minute)/bucketsize,0)*bucketsize)
	tltemp = np.array(list(CountFrequency(timelisttemp).items()))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Incidents', 
		mode="lines+markers"
	)

	data = go.Data([trace])
	labels="{'Minutes','Frequency'}"

	# Plot and embed in ipython notebook!
	#plotly.offline.iplot(data, filename='basic-plot')
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphBView(startdate,enddate,bucketsize):
	title='Graph B: Cases Frequency (in ' + str(bucketsize) +' minute facets)'

	timelist = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate)).values('caseDate').order_by())

	timelisttemp = sorted(round((pd.to_datetime(timelist['caseDate']).dt.hour*60+pd.to_datetime(timelist['caseDate']).dt.minute)/bucketsize,0)*bucketsize)
	tltemp = np.array(list(CountFrequency(timelisttemp).items()))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Cases',
		mode="lines+markers"
	)
	data = go.Data([trace])
	labels="{'Minutes','Frequency'}"

	# Plot and embed in ipython notebook!
	#plotly.offline.iplot(data, filename='basic-plot')
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphCView(startdate,enddate,starturg,endurg):
	title="Graph C: Incidents by Type (sorted by frequency)"

	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeCatId__catName').order_by())

	#datcount.append(i['crimeDate'].hour)
	timelisttemp = timelist['crimeCatId__catName']
	x=list(CountFrequency(timelisttemp).items())
	tltemp = np.array(sorted(x, reverse=True, key=lambda x: x[1]))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Incidents', 
		mode="lines+markers"
	)
	data = go.Data([trace])


	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphDView(startdate,enddate):
	title="Graph D: Cases by Type (sorted by frequency)"

	timelist = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate)
		).values('caseOffenseId__offenseCat').order_by())

	#datcount.append(i['crimeDate'].hour)
	timelisttemp = timelist['caseOffenseId__offenseCat']
	x=list(CountFrequency(timelisttemp).items())
	tltemp = np.array(sorted(x, reverse=True, key=lambda x: x[1]))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Cases Types', 
		mode="lines+markers"
	)
	data = go.Data([trace])


	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphEView(startdate,enddate,starturg,endurg):
	title="Graph E: Incident Type by Urgency (sorted by frequency)"

	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeCatId__catUrgency').order_by())

	#datcount.append(i['crimeDate'].hour)
	timelisttemp = timelist['crimeCatId__catUrgency']
	x=list(CountFrequency(timelisttemp).items())
	tltemp = np.array(sorted(x, reverse=True, key=lambda x: x[0]))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Severity', 
		mode="lines+markers"
	)
	data = go.Data([trace])
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphFView(startdate,enddate,officerbadge):
	title='Graph F: Cases by Officer (sorted by frequency)'

	if officerbadge == '':
		timelist = read_frame(Case.objects.filter(
			caseDate__range=(startdate,enddate)
			).values('caseOfficerId__officerName').order_by())
	else:
		timelist = read_frame(Case.objects.filter(
			caseDate__range=(startdate,enddate),
			caseOfficerId__officerBadge__exact=officerbadge
			).values('caseOfficerId__officerName').order_by())

	timelisttemp = timelist['caseOfficerId__officerName']
	x=list(CountFrequency(timelisttemp).items())
	tltemp = np.array(sorted(x, reverse=True, key=lambda x: x[1]))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Severity', 
		mode="lines+markers"
	)
	data = go.Data([trace])
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphGView(startdate,enddate,starturg,endurg):
	title='Graph G: Incidents count vs Weather'

	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeDate').order_by())

	timelisttemp = sorted(round(((pd.to_datetime(timelist['crimeDate']).dt.month-6)*30+pd.to_datetime(timelist['crimeDate']).dt.day),0))
	tltemp = np.array(list(CountFrequency(timelisttemp).items()))

	traces=[]
	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Incidents', 
		mode="lines+markers"
	)
	traces.append(trace)

	weatherfeed = [('wTempMax','Maximum Temperance'),
					('wDewMax','Maximum Dew'),
					('wHumidityMax','Maximum Humidity'),
					('wWindMax','Maximum Wind'),
					('wPressureMax','Maximum Pressure'),
					('wPrecipitation','Precipitation')]

	timelist = read_frame(Weather.objects.all())
	daynum=tltemp[0:,0]

	for (ifield, iline) in weatherfeed:
		timelisttemp = timelist[ifield]
		trace = go.Scatter(
			x=daynum,
			y=np.array(list(timelisttemp)),
			name=iline,  
			mode="lines+markers"
		)
		traces.append(trace)

	data = go.Data(traces)
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphHView(startdate,enddate):
	title='Graph H: Case count vs Weather'

	timelist = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		).values('caseDate').order_by())

	timelisttemp = sorted(round(((pd.to_datetime(timelist['caseDate']).dt.month-6)*30+pd.to_datetime(timelist['caseDate']).dt.day),0))
	tltemp = np.array(list(CountFrequency(timelisttemp).items()))

	traces=[]
	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Incidents', 
		mode="lines+markers"
	)
	traces.append(trace)

	weatherfeed = [('wTempMax','Maximum Temperance'),
					('wDewMax','Maximum Dew'),
					('wHumidityMax','Maximum Humidity'),
					('wWindMax','Maximum Wind'),
					('wPressureMax','Maximum Pressure'),
					('wPrecipitation','Precipitation')]

	timelist = read_frame(Weather.objects.all())
	daynum=tltemp[0:,0]

	for (ifield, iline) in weatherfeed:
		timelisttemp = timelist[ifield]
		trace = go.Scatter(
			x=daynum,
			y=np.array(list(timelisttemp)),
			name=iline,  
			mode="lines+markers"
		)
		traces.append(trace)

	data = go.Data(traces)
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphIView(startdate,enddate,starturg,endurg):
	title = 'Graph I: Weekly Incidents (starting Monday)'

	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeDate').order_by())

	timelisttemp = sorted(round(((pd.to_datetime(timelist['crimeDate']).dt.month-6)*30+pd.to_datetime(timelist['crimeDate']).dt.day),0))
	alldata = np.array(list(CountFrequency(timelisttemp).items()))

	traces=[]
	daynum = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	numweeks = int(round(len(alldata)/7,0))
	for itrace in range(numweeks):
		startweekday = itrace*7
		endweekday = (itrace*7)+6
		trace = go.Scatter(
			x=daynum,
			y=alldata[startweekday:endweekday,1],
			name='Incidents Week ' + str(itrace+1),  
			mode="lines+markers"
		)
		traces.append(trace)

	data = go.Data(traces)
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphJView(startdate,enddate):
	title = 'Graph J: Top offenses worked by top five officiers'
	topofficers = ['Martinez','Jackson','Burk','Allison','Caspers']

	topofficer = topofficers[0]
	officerbadge = Officer.objects.filter(
		officerName=topofficer
		).values('officerId').order_by()[0]['officerId']
	timelist0 = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		caseOfficerId__officerId__exact=officerbadge
		).values('caseOffenseId__offenseCat').order_by())

	topofficer = topofficers[1]
	officerbadge = Officer.objects.filter(
		officerName=topofficer
		).values('officerId').order_by()[0]['officerId']
	timelist1 = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		caseOfficerId__officerId__exact=officerbadge
		).values('caseOffenseId__offenseCat').order_by())

	topofficer = topofficers[2]
	officerbadge = Officer.objects.filter(
		officerName=topofficer
		).values('officerId').order_by()[0]['officerId']
	timelist2 = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		caseOfficerId__officerId__exact=officerbadge
		).values('caseOffenseId__offenseCat').order_by())

	topofficer = topofficers[3]
	officerbadge = Officer.objects.filter(
		officerName=topofficer
		).values('officerId').order_by()[0]['officerId']
	timelist3 = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		caseOfficerId__officerId__exact=officerbadge
		).values('caseOffenseId__offenseCat').order_by())

	topofficer = topofficers[4]
	officerbadge = Officer.objects.filter(
		officerName=topofficer
		).values('officerId').order_by()[0]['officerId']
	timelist4 = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate),
		caseOfficerId__officerId__exact=officerbadge
		).values('caseOffenseId__offenseCat').order_by())

	tlist = [timelist0,timelist1,timelist2,timelist3,timelist4]

	timelist = pd.concat(tlist)

	timelisttemp = timelist['caseOffenseId__offenseCat']
	x=list(CountFrequency(timelisttemp).items())
	tltemp = np.array(sorted(x, reverse=True, key=lambda x: x[1]))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Offense', 
		mode="lines+markers"
	)
	data = go.Data([trace])
	
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def GraphKView(startdate,enddate):
	title = 'Graph K: Processing Lag by Officier'

	timelist = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate)).values('caseDate','caseFileDate').order_by())

	timelisttemp = sorted(((pd.to_datetime(timelist['caseFileDate']).dt.month-6)*30+pd.to_datetime(timelist['caseFileDate']).dt.day)-
					((timelist['caseDate'].dt.month-6)*30+timelist['caseDate'].dt.day)
					)
	tltemp = np.array(list(CountFrequency(timelisttemp).items()))

	trace = go.Scatter(
		x=tltemp[0:,0],
		y=tltemp[0:,1],
		name='Case Filing Lags',
		mode="lines+markers"
	)
	data = go.Data([trace])
	labels="{'Minutes','Frequency'}"

	# Plot and embed in ipython notebook!
	#plotly.offline.iplot(data, filename='basic-plot')
	plot_div = plot(data, output_type='div', show_link=False, include_plotlyjs=False)

	return (title, plot_div)

def MapAView(startdate,enddate,starturg,endurg):
	title = 'Map A: Heat Map of Incidents'

	starturg=3
	endurg=5
	timelist = read_frame(Crime.objects.filter(
		crimeDate__range=(startdate,enddate),
		crimeCatId__catUrgency__gte=starturg,
		crimeCatId__catUrgency__lte=endurg).values('crimeLat','crimeLong'))

	latitude_list = timelist['crimeLat']
	longitude_list = timelist['crimeLong']

	# center co-ordinates of the map 
	gmap = gmplot.GoogleMapPlotter( 35.221770,-97.444960,13)

	# plot the co-ordinates on the google map 
	gmap.scatter( latitude_list, longitude_list, size = 40, marker = True) 

	# the following code will create the html file view that in your web browser 
	gmap.heatmap(latitude_list, longitude_list) 

	gmap.draw( "dashboard/templates/dashboard/heatmapinc.html" )

	return ('')

def MapBView(startdate,enddate):
	title = 'Map B: Heat Map of Cases'

	timelist = read_frame(Case.objects.filter(
		caseDate__range=(startdate,enddate)
		).values('caseLat','caseLong'))

	latitude_list = timelist['caseLat']
	longitude_list = timelist['caseLong']

	# center co-ordinates of the map 
	gmap = gmplot.GoogleMapPlotter( 35.221770,-97.444960,13)

	# plot the co-ordinates on the google map 
	gmap.scatter( latitude_list, longitude_list, size = 40, marker = True) 

	# the following code will create the html file view that in your web browser 
	gmap.heatmap(latitude_list, longitude_list) 

	gmap.draw( "dashboard/templates/dashboard/heatmapcase.html" )

	return ('')

def AdjustGraphView(request):
	#form = GraphTypeForm()

	if request.method == "POST":
		form = GraphTypeForm(request.POST)
		if form.is_valid():
			graphpara = form.save(commit=False)
			graphpara.save()
			return redirect('dashboard-home')
	else:
		form = GraphTypeForm()

	return render(request, 'dashboard/graphadjust.html', {'form': form})

def SelectGraphView(request):
	# declaring template
	template = "dashboard/graphinput.html"

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = GraphTypeForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			

			# redirect to a new URL:
			return HttpResponseRedirect( "dashboard/graphinput.html" )

	# If this is a GET (or any other method) create the default form.
	else:
		title = ''


	#fig.show()
	context = {

	}
	return render(request, "dashboard/graphinput.html", context)

def HeatMapIncView(request):
	# declaring template
	template = "dashboard/heatmapinc.html"

	#fig.show()
	context = {

	}
	return render(request, "dashboard/heatmapinc.html", context)

def HeatMapCaseView(request):
	# declaring template
	template = "dashboard/heatmapcase.html"

	#fig.show()
	context = {

	}
	return render(request, "dashboard/heatmapcase.html", context)

def home(request):
	cstzone=pytz.timezone("America/Chicago")  # Time zone of Norman, OK
	lastinput = Graphdata.objects.last()
	bucketsize = getattr(lastinput,'bucket_Size')
	startdate=getattr(lastinput,'start_Date')
	enddate=getattr(lastinput,'end_Date')
	starturg=getattr(lastinput,'start_Urgency')
	endurg=getattr(lastinput,'end_Urgency')

	plotcnt = 0
	titles=[]
	plots=[]

	(title, plot_div) = GraphAView(startdate,enddate,starturg,endurg,bucketsize)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphBView(startdate,enddate,bucketsize)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphCView(startdate,enddate,starturg,endurg)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphDView(startdate,enddate)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphEView(startdate,enddate,starturg,endurg)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	officerbadge = ''
	(title, plot_div) = GraphFView(startdate,enddate,officerbadge)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphGView(startdate,enddate,starturg,endurg)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphHView(startdate,enddate)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphIView(startdate,enddate,starturg,endurg)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphJView(startdate,enddate)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1

	(title, plot_div) = GraphKView(startdate,enddate)
	titles.append(title)
	plots.append(plot_div)
	plotcnt+=1


	MapAView(startdate,enddate,starturg,endurg)  #displayed in its own page

	MapBView(startdate,enddate)  #displayed in its own page

	mylist=zip(titles,plots)
	context = {
		'bucketsize': bucketsize,
		'startdate': startdate,
		'enddate': enddate,
		'starturg': starturg,
		'endurg': endurg,
		'mylist': mylist
	}

	return render(request, "dashboard/home.html", context)

def GraphListView(request):

	crime = Crime.objects.all()[:100]
	
	#fig = px.bar(crime, x='minute', y='count', 
	#					name='Crime over time in a day',
	#					hover_data=['crimeDate', 'crimeCatId'],
	#					labels={'pop':'Frequecy'},
	#					opacity=0.8, marker_color='lifeExp')

	#plot_div = plot(fig, output_type='div', show_link=False, include_plotlyjs=False)

	#return render(request, "dashboard/home.html", context={'plot_div': plot_div})

def plot_1_hover(self, points, **event_args):
  """This method is called when a data point is hovered."""
  print(f"User hovered over x:{points[0]['x']} and y:{points[0]['y']}")


def about(request):
	return render(request, 'dashboard/about.html', {'title': 'About'})

def mymaps(request):  # GPS heat maps

	# declaring template
	template = "dashboard/mymaps.html"
	
	context = {}
	return render(request, "dashboard/home.html", context)