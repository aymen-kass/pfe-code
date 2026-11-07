from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('logoutUser/',views.logoutUser, name="logoutUser"),
    path('test/',views.test, name="test"),
    path('addtest/',views.createTest, name="addtest"),
]
