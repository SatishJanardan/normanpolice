from django.urls import path
from .views import (
    pdf_norman,
    csv_weather,
    update_gps,
)

from . import views

urlpatterns = [
    path('', views.pdf_norman, name='imports-home'),
    path('reports/', views.pdf_norman, name="imports-home"),
    path('weather/', views.csv_weather, name="imports-csv_weather"),
    path('update_gps/', views.update_gps, name="imports-update_gps"),
    path('about/', views.about, name='imports-about'),
]

