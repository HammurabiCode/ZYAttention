"""AttProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
# from AttApp.views import *
import AttApp.zhy_views
import AttApp.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', AttApp.views.index),
    url(r'^test/', AttApp.views.test),
    url(r'^test_detail/', AttApp.views.test_detail),
    url(r'^quiz/', AttApp.views.quiz),
    url(r'^quiz_test/', AttApp.views.quiz_test),
    url(r'^quiz_test_detail/', AttApp.views.quiz_test_detail),
    url(r'^download_student/', AttApp.views.download_student),
    
    url(r'^stu_list/', AttApp.views.stu_list),
    url(r'^test_lib', AttApp.views.test_lib),
    url(r'^init_db/', AttApp.views.init_db),
    url(r'^clear_db/', AttApp.views.clear_db),
]
