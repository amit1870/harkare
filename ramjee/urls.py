from django.urls import path

from . import views

app_name = 'ramjee'
urlpatterns = [
    path('harkare/upload/', views.upload_harkara, name='upload'),
    path('harkare/', views.list_harkare, name='harkare'),

]