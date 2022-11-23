from django.urls import path
from . import views 
from . import scraping

urlpatterns = [
    path('', views.callback),
    path('scraping/', scraping.ScrapingView)
]