
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.gallery, name='gallery'),
	url(r'^detail/', views.image_detail, name='detail'),
]

