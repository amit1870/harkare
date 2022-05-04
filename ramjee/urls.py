from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r'harkare', views.HarkareList)

app_name = 'ramjee'
urlpatterns = [
    path('harkare/upload/', views.upload_harkara, name='upload'),
    path('harkare/donation/', views.donation, name='donation'),
    path('harkare/limit/', views.show_limitation, name='limitation'),
    path('harkare/', views.list_harkare, name='harkare'),
    # path('', include(router.urls)),

]
