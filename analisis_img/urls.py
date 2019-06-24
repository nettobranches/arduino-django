from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_single', views.upload_single, name="upload_single")
]