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

from police.models import OffenseCat, Officer, Case, Weather

# Create your views here.
def home(request):
	context = {
		cases: Case.objects.all()
	}
	return render(request, 'case/home.html', context)

class CaseListView(ListView):
	model = Case
	template_name = 'case/home.html'
	context_object_name = 'cases'
	paginate_by = 15

class CaseDetailView(DetailView):
	model = Case

class CaseCreateView(LoginRequiredMixin, CreateView):
	model = Case
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author =self.request.user
		return super().form_valid(form)


class CaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Case
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		case = self.get_object()
		if self.request.user == case.author:
			return True
		return False

class CaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Case
    success_url = '/'

    def test_func(self):
        case = self.get_object()
        if self.request.user == case.author:
            return True
        return False

class CasePostListView(ListView):
	model = Case
	template_name = 'case/case_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['caseDate']
	paginate_by = 15

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Case.objects.filter(author=user).order_by('caseDate')

def about(request):
   return render(request, 'case/about.html', {'title': 'About'})
