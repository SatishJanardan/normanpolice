from django.urls import path
from .views import (
    GraphListView,
    AdjustGraphView,
    SelectGraphView,
    HeatMapIncView,
    HeatMapCaseView,
    csv_upload,
    mymaps
)

from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('graph/', views.SelectGraphView, name="dashboard-graph"),
    path('upload-csv/', views.csv_upload, name="dashboard-csv_upload"),
    path('mymaps/', views.mymaps, name="dashboard-mymaps"),
    path('graphadjust/', views.AdjustGraphView, name="dashboard-graphadjust"),
    path('heatmapinc/', views.HeatMapIncView, name="dashboard-heatmapinc"),
    path('heatmapcase/', views.HeatMapCaseView, name="dashboard-heatmapcase"),
    path('about/', views.about, name='dashboard-about'),
]

