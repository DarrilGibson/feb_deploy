from django.conf.urls import url
from . import views
# from django.contrib import admin

app_name = "loginreg"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^show$', views.show, name="show"),
    url(r'^success$', views.success, name="success"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^show/(?P<id>\d+)/delete$', views.destroy, name="destroy"),
    url(r'^show/(?P<id>\d+)/edit$', views.edit, name="edit"),
    url(r'^edituser$', views.edituser, name="edituser"),
]
