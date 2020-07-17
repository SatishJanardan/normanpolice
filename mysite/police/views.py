from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from plotly.offline import plot
from plotly.graph_objs import Scatter

from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView,
	DeleteView
)

from .models import Cat, Crime


# police functions
def home(request):
	context = {
		crimes: Crime.objects.all()
	}
	return render(request, 'dashboard/home.html', context)

class CrimeListView(ListView):
	model = Crime
	template_name = 'dashboard/home.html'
	context_object_name = 'crimes'
	paginate_by = 20

def about(request):
   return render(request, 'police/about.html', {'title': 'About'})
