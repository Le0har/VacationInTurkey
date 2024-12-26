from django.urls import path
from vacation import views


app_name = 'vacation'

urlpatterns = [
    path('', views.index_page, name='home'),
]
