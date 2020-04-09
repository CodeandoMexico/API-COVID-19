from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suspected', views.suspected, name='suspected'),
    path('last_origin', views.last_origin, name='last_origin'),
]