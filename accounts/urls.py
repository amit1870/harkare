from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.register, name='register'),
    path('siyaram', views.siyaram, name='siyaram'),
    path('success', views.success, name='success'),
    path('login/', views.account_login, name='login'),
    path('logout', views.account_logout, name='logout'),
    path('activate/<str:hex_code>', views.activate, name='activate'),

]