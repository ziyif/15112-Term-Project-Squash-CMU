from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^partner$', views.partner, name='partner'),
    url(r'^signup$', views.signup, name='signup'),

    #app/11/
    url(r'^(?P<user_id>[0-9]+)/$',views.profile,name='profile'),


    url(r'^player-form$', views.PlayerCreate.as_view(), name='player-form'),




]