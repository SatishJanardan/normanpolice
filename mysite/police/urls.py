from django.urls import path
from .views import (
	CrimeListView
)
from . import views

urlpatterns = [
    path('', CrimeListView.as_view(), name='dashboard-home'),
    path('about/', views.about, name='police-about'),
]

