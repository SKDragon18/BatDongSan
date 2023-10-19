from django.urls import path
from . import views


urlpatterns = [
    path("", views.login.as_view(),name='login'),
    path("register",views.createAccount.as_view(),name='register'),
    path("getCode",views.createAccount.as_view(),name='getCode'),
    path("checkCode",views.checkCode.as_view(),name='checkCode'),
    path("send", views.sendMail,name="sendMail"),
    path("info",views.info,name="info"),
    path("forgot",views.forgot.as_view(),name="forgot")
]