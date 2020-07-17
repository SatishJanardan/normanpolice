from django.db import models
from police.models import Filelist, Cat, Crime, OffenseCat, Officer, Arrest, Case
from datetime import datetime

import plotly.graph_objects as go
# from votes import wide as df
import plotly.express as px
data = px.data.gapminder()

data_canada = data[data.country == 'Canada']
fig = px.bar(data_canada, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
             labels={'pop':'population of Canada'}, height=400)
fig.show()
error()

'''
def plot_1_hover(self, points, **event_args):
	"""This method is called when a data point is hovered."""
	print(f"User hovered over x:{points[0]['x']} and y:{points[0]['y']}")

	# Plot some data
	self.plot_1.data = [
	  go.Scatter(
	    x = [1, 2, 3],
	    y = [3, 1, 6],
	    marker = go.Marker(
	      color= 'rgb(16, 32, 77)'
	    )
	  ),
	  go.Bar(
	    x = [1, 2, 3],
	    y = [3, 1, 6],
	    name = 'Bar Chart Example'
	  )
	]

# Tell Plotly to render it
fig.show()

#  Get a convenient list of x-values
x = Crime.objects.filter(crimeDate)



exit()
years = df['year']
x = list(range(len(years)))

# Specify the plots
bar_plots = [
    go.Bar(x=x, y=df['conservative'], name='Conservative', marker=go.bar.Marker(color='#0343df')),
    go.Bar(x=x, y=df['labour'], name='Labour', marker=go.bar.Marker(color='#e50000')),
    go.Bar(x=x, y=df['liberal'], name='Liberal', marker=go.bar.Marker(color='#ffff14')),
    go.Bar(x=x, y=df['others'], name='Others', marker=go.bar.Marker(color='#929591')),
]

# Customise some display properties
layout = go.Layout(
    title=go.layout.Title(text="Election results", x=0.5),
    yaxis_title="Seats",
    xaxis_tickmode="array",
    xaxis_tickvals=list(range(27)),
    xaxis_ticktext=tuple(df['year'].values),
)

# Make the multi-bar plot
fig = go.Figure(data=bar_plots, layout=layout)

# Tell Plotly to render it
fig.show()
'''
