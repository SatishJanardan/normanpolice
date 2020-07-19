from django.urls import path
from .views import (
    CaseListView, 
    CaseDetailView,
    CaseCreateView,
    CaseUpdateView,
    CaseDeleteView,
    CasePostListView,
)
from . import views

urlpatterns = [
    path('', CaseListView.as_view(), name='case-home'),
    path('case/<int:pk>/', CaseDetailView.as_view(), name='case-detail'),
    path('caseuser/<str:username>', CasePostListView.as_view(), name='case-posts'),
    path('case/new/', CaseCreateView.as_view(), name='case-create'),
    path('case/<int:pk>/update', CaseUpdateView.as_view(), name='case-update'),
    path('case/<int:pk>/delete', CaseDeleteView.as_view(), name='case-delete'),
    path('about/', views.about, name='case-about'),
]

