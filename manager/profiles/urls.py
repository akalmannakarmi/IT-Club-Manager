from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:profileId>', views.viewProfile, name='viewProfile'),
    path('myProfile', views.viewMyProfile, name='viewMyProfile'),
    path('saveProfile', views.saveProfile, name='saveProfile'),
]
