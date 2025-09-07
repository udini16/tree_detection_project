from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('streetview/', views.streetview, name='streetview'),
    path('streetview/scan/', views.streetview_scan, name='streetview_scan'),
]
