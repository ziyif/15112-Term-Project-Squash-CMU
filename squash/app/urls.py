from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),

    url(r'^match_history/(?P<player_id>[0-9]+)/$', views.match_history, name='match_history'),
    url(r'^partner$', views.partner, name='partner'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^update$', views.updateProfile, name='update'),
    url(r'^filter$', views.filter, name='filter'),
    url(r'^match_result$', views.match_result, name='match_result'),


    #app/11/
    # url(r'^(?P<user_id>[0-9]+)/$',views.profile,name='profile'),
    url(r'^user/(?P<player_id>[0-9]+)/$', views.profile, name='profile'),

    # url(r'^user/(?P<pk>[0-9]+)/$', views.PlayerProfileDetail.as_view(), name='player_profile_detail'),
    # url(r'^user/(?P<pk>[0-9]+)/update/$', views.PlayerProfileUpdate.as_view(), name='player_profile_edit'),
    # url(r'^player-form$', views.PlayerCreate.as_view(), name='player-form'),




]