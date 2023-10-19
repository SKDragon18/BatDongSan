"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views
# app_name='nguoidung'
urlpatterns = [
    path('', views.index),
    path('home',views.home),
    path('dang_tin/<str:loai>',views.DangTin.as_view(),name='dang_tin'),
    path('xem_ds',views.DanhSachBaiDang.as_view(),name='xem_ds'),
    path('xem_chitiet/<int:id_baidang>',views.xem_chitiet,name='xem_chitiet'),
    path('go_baidang/<int:id_baidang>',views.GoBaiDang.as_view(),name='go_baidang'),
    path('xem_ds_yeuthich',views.DanhSachYeuThich.as_view(),name='xem_ds_yeuthich'),
    path('unfollow/<int:id_baidang>',views.unfollow,name='unfollow'),
    path('admin/ds_duyet',views.DanhSachDuyet.as_view(),name='ds_duyet'),
    path('admin/ds_duyet/<int:id_baidang>',views.DuyetBaiDang.as_view(),name='duyet_baidang'),
    path('logout',views.logout,name='logout'),
    path('test',views.test,name='test')
]
