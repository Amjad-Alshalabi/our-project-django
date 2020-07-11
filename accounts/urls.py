from django.urls import path , include
from . import views
from django.conf.urls import url , re_path
from django.contrib.auth import  login , logout
from django.contrib.auth.views import LoginView ,LogoutView
from accounts.views import signup , activate

app_name='accounts'
urlpatterns = [
    # path("login", views.do_login, name="login"),
    path('signup/', signup, name="signup"),
    path('activate/<slug:uidb64>/<slug:token>/',activate, name='activate'),
]
