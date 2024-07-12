from . import views
from django.urls import path
from .functions import Requests_Navbar

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout_user, name='logout'),
    path('profile/<int:pk>/',views.profile,name='profile'),
    path('modify/',views.modify_aacount,name='modify'),
    path('leaderboard',views.ranking, name='ranking'),
    path('add_friiends/',views.adding_friends, name="add_friends"),
    path('create_group/',views.Create_Group , name='create_group'),
    path('poop_group/<int:pk>/', views.Group_Popp_View , name='group_poop'),
    path('navbar/handle_request/',Requests_Navbar, name='navbar')
]