from django.urls import path
from .views import (
    GraphListView,
    SelectGraphView,
    csv_upload,
    mymaps
)

from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('graph/', views.SelectGraphView, name="dashboard-graph"),
    path('upload-csv/', views.csv_upload, name="dashboard-csv_upload"),
    path('mymaps/', views.mymaps, name="dashboard-mymaps"),
    path('about/', views.about, name='dashboard-about'),
]

