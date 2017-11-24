from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)

app_name = 'core'

urlpatterns = [

    url(r'^$', views.login_redirect, name="login_redirect"),
    url(r'^profile/password/$', views.change_password_redirect, name='change_password_redirect'),
    url(r'^login/$', views.login, name="login"),
    url(r'^auth/$', views.auth_view, name="auth"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^invalid/$', views.invalid_login, name="invalid"),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^register_success/$', views.register_success, name="register_success"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^edit_habilidades/(?P<pk>[0-9]+)/$', views.edit_habilidades, name='edit_habilidades'),
    url(r'^home/$', views.post_list, name='home'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),    


    url(r'^reset-password/$', password_reset, {'template_name': 'reset_password.html', 'post_reset_redirect': '/reset-password/done', 'email_template_name': 'reset_password_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'reset_password_done.html'}, name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'reset_password_confirm.html', 'post_reset_redirect': '/reset-password/complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'reset_password_complete.html'}, name='password_reset_complete'),




    
    #url(r'^teste/$', views.teste, name="teste"),

]
