from django.urls import path
from . import views

urlpatterns = [
    path('terminal/', views.ViewTerminal.as_view(), name='terminal'),
    path('webclient/', views.ViewWebClient.as_view(), name='webclient'),
]
