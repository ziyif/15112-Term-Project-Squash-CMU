from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),


    url(r'^match_history/(?P<player_id>[0-9]+)/$', views.match_history, name='match_history'),
    url(r'^match_history_opponent/(?P<player_id>[0-9]+)/(?P<opponent_id>[0-9]+)/$', 
                views.match_history_opponent, name='match_history_opponent'),
    url(r'^enter_result$', views.enter_result, name='enter_result'),


    url(r'^success$', views.success, name='success'),
    url(r'^result_confirmation$', views.result_confirmation, name='result_confirmation'),




    url(r'^ladder$', views.ladder, name='ladder'),

    url(r'^partner$', views.partner, name='partner'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^update$', views.updateProfile, name='update'),
    url(r'^filter$', views.filter, name='filter'),
    url(r'^match_result$', views.match_result, name='match_result'),

    url(r'^user/(?P<player_id>[0-9]+)/$', views.profile, name='profile'),



]