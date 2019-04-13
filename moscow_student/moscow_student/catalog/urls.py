from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^autolike/$', views.autolike, name='autolike'),
    url(r'^authorization/',views.authorization, name='authorization'),
]