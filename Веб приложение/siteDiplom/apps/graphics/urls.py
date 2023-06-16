from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show, name='show'),
    path('', views.main, name='main'),
    path('graphics/', views.index, name='index'),
]
