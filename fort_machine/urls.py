"""fort_machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from audit import views
from django.conf.urls.static import serve
from fort_machine import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.my_login),
    path('',views.index),
    # path('logout/',views.my_logout),
    # path('log/',views.my_log),
    path('register/',views.register),
    path('host_list/',views.host_list,name='host_list'),
    path('multitask/cmd/',views.multi_cmd,name='multi_cmd'),
    path('api/host_list/',views.ajax_host,name='get_host_list'),
    path('api/token/',views.ajax_token,name='get_token'),
    path('multitask/result',views.task_result,name='task_result'),
    path('multitask',views.multi_task,name='multitask'),
    path('multi_files_transfer',views.multi_files_transfer,name='multi_files_transfer'),
    path('task_file_download',views.task_file_download,name='task_file_download'),
    path('task_file_upload',views.task_file_upload,name='task_file_upload'),









    # re_path(r'media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_ROOT,'show_indexes':True}), #公共文件数据路径接口（下载地址），serve 是django内置的视图函数，外加默认参数详细查看serve视图函数
    # path('login/',views.my_login),
]
