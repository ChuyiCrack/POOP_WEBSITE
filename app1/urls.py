from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout_user, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('modify/',views.modify_aacount,name='modify')
]