
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from community.views import create as createCommunity
from community.views import topCommunities, trendingCommunities
from posts.views import (createArticle, createThread, deleteReply_AJAX,
                         replyVoteToggle_AJAX, updateReply_AJAX,
                         postVoteToggle_AJAX, postSaveToggle_AJAX)
from users.views import (deleteAccount_AJAX, emailVerify, login, register,
                         settings, validateEmail_AJAX, modpanel)
from .views import home, latest, suggested, top, popular, search_view


# url patterns under ('')
urlpatterns = [

    # base site urls
    path('', home, name='home'),
    path('top/', top, name='top'),
    path('latest/', latest, name='latest'),
    path('popular/', popular, name='popular'),
    path('suggested/', suggested, name='suggested'),
    path('top-communities/', topCommunities, name='top-communities'),
    path('trending-communities/', trendingCommunities, name='trending-communities'),

    # search url
    path('search/<str:search_qry>', search_view, name='search'),
    
    # user app login/logout and signup urls
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('register/test-email/', validateEmail_AJAX, name='test-email'),

    # user/profile action urls
    path('settings/', settings, name='settings'),
    path('modpanel/', modpanel, name='modpanel'),
    path('settings/delete/', deleteAccount_AJAX, name="account-delete"),
    re_path(r'^email_verify/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', emailVerify, name='email-verify'),

    # user password-reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password-reset-complete'),

    # content creation urls
    path('create/community/', createCommunity, name="create-community"),
    path('create/article/', createArticle, name="create-article"),
    path('create/thread/', createThread, name="create-thread"),
    path('create/post/', createThread, name="create-post"),

    # reply action urls
    path('reply/update/', updateReply_AJAX, name='reply-update'),
    path('reply/delete/', deleteReply_AJAX, name='reply-delete'),
    path('reply/vote/', replyVoteToggle_AJAX, name='reply-vote'),

    # post action urls
    path('post/vote/', postVoteToggle_AJAX, name='post-vote'),
    path('post/save/', postSaveToggle_AJAX, name='post-save'),

]