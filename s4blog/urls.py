"""s4blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from app02 import views as views2
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth-login.html$', views2.login),
    url(r'^auth-index.html$', views2.index),
    url(r'^auth-menu.html$', views2.menu),



    url(r'^all/(?P<type_id>\d+)/', views.index),
    url(r'^login/', views.login),
    url(r'^check_code/', views.check_code),
    url(r'^register/', views.register),
    url(r'^up.html$', views.up),

    url(r'^see.html$', views.see),
    url(r'^upload_img.html$', views.upload_img),
    # url(r'^lizhi-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<article2tag__tag_id>\d+).html$', views.lizhi),
    url(r'^wangzhe.html$', views.wangzhe),
    url(r'^comments-(\d+).html$', views.comments),
    url(r'^lizhi-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', views.lizhi),

    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', views.article),
    url(r'^(?P<site>\w+)/(?P<key>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/', views.filter),
    url(r'^(\w+)/$', views.home),
    url(r'^register/', views.register),
    url(r'^', views.index),
]
