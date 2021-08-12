"""ckweb_background URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from api.views import *
# from django.conf.urls.static import static
from django.views import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/Sign', AuthView.as_view()),
    path('api/register', register),   # 登录传入参数user，pwd
    path('api/Sign2', OrderView.as_view()),

    path('api/img', user_Img), #上传数据
    #文章类
    path('api/data', all_data.as_view()), # 查询所以文章
    path('api/picture', notall_data), # 没登录查询所以文章
    path('api/upData', Imgnotice),   # 更新文章
    path('api/idData', check_data), # 根据ip查询文章
    # 视频类
    path('api/VideoUpData', UPvideoNotice),   # 更新视频
    path('api/VideoData', video_all_data.as_view()),   # 查询所以视频
    path('api/video', notvideo_all_data),   # 没登录查询所以视频

    path('api/VideoIdData', video_check_data), # 根据ip查询视频

    path('api/homeImg', Home_img.as_view()),  # 首页视频
    path('api/front', notHome_img),  # 没登录首页视频
    path('api/Introduction', Introduction_img.as_view()),  # 首页视频
    path('api/infoIntroduction', notIntroduction_img),  # 首页视频

    # 访问量
    path('api/userValue', userValue),

    path('api/test', stream_video),

    url(r'^api/static/(?P<path>.*)$', static.serve,
    {'document_root': settings.STATIC_ROOT}, name='static'),
]
# Cannot import ASGI_APPLICATION module 'ckweb_background.routing'