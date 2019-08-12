from django.urls import path

from . import views

app_name='crud'
urlpatterns = [

    path('' ,views.index,name='index'),
    path('user_login/' ,views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('update/',views.update,name='update'),
    path('delete/',views.delete,name='delete'),
]