from django.conf.urls import url
from . import views 

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'login$', views.login),
	url(r'^myaccount/(?P<id>\d+)$', views.edit),
	url(r'^myaccount/(?P<id>\d+)/edit/$', views.editpage),
	url(r'^display$', views.display),
	url(r'^addtrip$', views.addtrip),
	url(r'^addtrip_db$', views.addtrip_db),
	url(r'^cancel/(?P<id>\d+)$', views.cancel),
	url(r'^delete/(?P<id>\d+)$', views.delete),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^views/(?P<id>\d+)', views.view)
]

