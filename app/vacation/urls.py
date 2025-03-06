from django.urls import path
from vacation import views


app_name = 'vacation'

urlpatterns = [
    path('', views.index_page, name='index'),
    path('photos/antalya', views.antalya_list, name='antalya-list'),
    path('photos/side', views.side_list, name='side-list'),
    path('photos/kemer', views.kemer_list, name='kemer-list'),
    path('photos/<int:photo_id>', views.photo_detail, name='photo-detail'),
    path('register', views.create_user, name='register'),
]
