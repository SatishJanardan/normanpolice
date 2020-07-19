from django.urls import path
from .views import (
	CrimeListView, 
	CrimeDetailView,
	CrimeCreateView,
	CrimeUpdateView,
	CrimeDeleteView,
    CrimePostListView,
)
from . import views

urlpatterns = [
    path('', CrimeListView.as_view(), name='incident-home'),
    path('incident/<int:pk>/', CrimeDetailView.as_view(), name='incident-detail'),
    path('incidentuser/<str:username>', CrimePostListView.as_view(), name='crime-posts'),
    path('incident/new/', CrimeCreateView.as_view(), name='incident-create'),
    path('incident/<int:pk>/update', CrimeUpdateView.as_view(), name='incident-update'),
    path('incident/<int:pk>/delete', CrimeDeleteView.as_view(), name='incident-delete'),
    path('about/', views.about, name='incident-about'),
]

