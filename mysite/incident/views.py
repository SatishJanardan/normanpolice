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

from police.models import Cat, Crime, Weather

# incident functions
def home(request):
	context = {
		crimes: Crime.objects.all()
	}
	return render(request, 'incident/home.html', context)

class CrimeListView(ListView):
	model = Crime
	template_name = 'incident/home.html'
	context_object_name = 'crimes'
	paginate_by = 15

class CrimeDetailView(DetailView):
	model = Crime

class CrimeCreateView(LoginRequiredMixin, CreateView):
	model = Crime
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author =self.request.user
		return super().form_valid(form)


class CrimeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Crime
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		crime = self.get_object()
		if self.request.user == crime.author:
			return True
		return False

class CrimeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Crime
    success_url = '/'

    def test_func(self):
        crime = self.get_object()
        if self.request.user == crime.author:
            return True
        return False

class CrimePostListView(ListView):
	model = Crime
	template_name = 'incident/crime_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['crimeDate']
	paginate_by = 15

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Crime.objects.filter(author=user).order_by('crimeDate')

def about(request):
   return render(request, 'incident/about.html', {'title': 'About'})
