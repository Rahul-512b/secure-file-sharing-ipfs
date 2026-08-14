"""
URL configuration for ipfs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from page import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.signup_view,name='signup'),
    path('login/',v.login_view,name='login'),
    path('home/',v.home,name='home'),
    path('logout/',v.logout_view,name='logout'),
    path('request/<int:file_id>/',v.request_view,name="request_view"),
    path('grantaccess/<int:requester_id>/<int:file_id>/',v.grant_access,name='grant_access'),
    path('revoke_access/<int:requester_id>/<int:file_id>/',v.revoke_access,name="revoke_access"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
