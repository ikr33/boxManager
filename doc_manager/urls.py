"""doc_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from filebrowser.sites import site
from django.conf.urls import url
from filemanager import path_end
from django.urls import path, re_path


urlpatterns = [
    path ('admin/filebrowser/',site.urls),
    path ('grappelli/', include ('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name="register"),
    path('profile/',user_views.profile,name="profile"),
    path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),
    path('blog/', include('blog.urls')),
    path('', include('docs.urls')),
    url(r'^docs/browse/filemanager' + path_end, user_views.viewimages, name='viewimages'),
    url(r'^docs/browse/'+path_end,user_views.view, name='view'),
   # url(r'^docs/share/'+'(?P<id>[0-9])'+'/(?P<path>[\w\d_ -/.]*)$', user_views.share, name='share'),
#    re_path(r'^docs/share/' + '(<int:id>)' + '/(?P<path>[\w\d_ -/.]*)$', user_views.share, name='share'),

    url(r'^docs/generate/' + '(?P<id>[0-9]+)' + '/(?P<path>[\w\d_ -/.]*)$', user_views.generate, name='generate'),
   #url(r'^docs/share/' + '(?P<id>[0-9]{3})' + '/(?P<path>[\w\d_ -/.]*)$', user_views.share, name='share'),


    url(r'^docs/share/(?P<link>[\S\-]+)/$',user_views.share, name="share"),
    url(r'^docs/viewshared/filemanager' + path_end, user_views.viewimages, name='viewimages'),
    url(r'^docs/viewshared/(?P<path>[\S\-]+)/$', user_views.viewshared, name="viewshared"),
    url(r'^docs/viewshared/$', user_views.viewshared, name="viewshared1"),
    #url(r'^docs/viewshared/(?P<path>[\w\d_ -/.]*)$', user_views.viewshared, name="viewshared")

    url(r'^docs/emailshare/$', user_views.sharebyemail, name="emailshare"),
    url(r'^docs/smsshare/$', user_views.sharebysms, name="smsshare"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
