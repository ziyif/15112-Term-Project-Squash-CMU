from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^partner$', views.partner, name='partner'),
    url(r'^signup$', views.signup, name='signup')

]