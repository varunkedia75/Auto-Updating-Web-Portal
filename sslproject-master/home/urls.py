from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='home'),
    # url(r'login/$', views.login),
    # url(r'login/$', views.login, name='login'),
    # url(r'signup/$', views.signup),
    # url(r'^login/$', views.UserFormView.as_view(), name='register'),
]