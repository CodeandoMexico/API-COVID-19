from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suspected', views.suspected, name='suspected'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('last_origin', views.last_origin, name='last_origin'),
]