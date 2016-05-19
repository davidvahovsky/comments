"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from articles.views import CommentListView, ArticleDetailView, SubCommentListView, CommentLikeView, \
    CommentDislikeView, comment_create, subcomment_create, add_form

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^article/(?P<pk>[\w-]+)/?$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^article/(?P<pk>[\w-]+)/comments/?$', CommentListView.as_view(), name='comment_list'),
    url(r'^article/(?P<pk>[\w-]+)/add_comment/?$', comment_create, name='comment_create'),
    url(r'^article/(?P<pk>[\w-]+)/comment/(?P<com_pk>[\w-]+)/add_comment/?$', subcomment_create, name='subcomment_create'),
    url(r'^article/(?P<pk>[\w-]+)/comment/(?P<com_pk>[\w-]+)/form/?$', add_form, name='add_form'),
    url(r'^article/(?P<pk>[\w-]+)/comment/(?P<com_pk>[\w-]+)/comments/?$',
        SubCommentListView.as_view(), name='sub_comment_list'),
    url(r'^comment/(?P<pk>[\w-]+)/like/?$', CommentLikeView.as_view(), name='comment_like'),
    url(r'^comment/(?P<pk>[\w-]+)/dislike/?$', CommentDislikeView.as_view(), name='comment_dislike'),
]