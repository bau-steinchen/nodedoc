from django.urls import path
from .views import nodes_list

urlpatterns = [
    path('', nodes_list, name='nodes_list'),
]
