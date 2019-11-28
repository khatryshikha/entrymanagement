from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^host_details', views.host_details, name='host_details'),
    url(r'^visitor_details', views.visitor_details, name='visitor_details'),
    url(r'^visitor_checkout/(?P<id>[\w\-]+)/',
        views.checkout, name='checkout'),
]
