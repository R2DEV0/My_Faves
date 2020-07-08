from django.urls import path     
from . import views
	
urlpatterns = [
	path('', views.index),
	path('new_user', views.new_user),
    path('login', views.login),
    path('main/<int:user_id>', views.main),
    path('logout', views.logout),
    path('newcity/<int:user_id>', views.NewCity),
    path('addnewcity', views.addNewCity),
    path('removecity/<int:city_id>', views.removeCity),
    path('citydetail/<int:city_id>', views.cityDetails),
    path('search/<int:city_id>', views.search),
    path('faveIt/<int:city_id>/<str:business_name>', views.faveIt),
    path('removeFave/<int:fave_id>/<int:city_id>', views.removeFave),

]