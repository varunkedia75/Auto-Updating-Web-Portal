from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<department>\w+)/$', views.homepage),
    url(r'^(?P<department>\w+)/allfaculty', views.all_faculty),
    url(r'^(?P<department>\w+)/headofdepartment', views.headofdepartment),
    url(r'^(?P<department>\w+)/prof', views.prof),
    url(r'^(?P<department>\w+)/associate_prof', views.associate_prof),
    url(r'^(?P<department>\w+)/assistant_prof', views.assistant_prof),
    url(r'^(?P<department>\w+)/visiting_faculty', views.visiting_faculty),
    url(r'^facultypage/(?P<user>\w+)/$', views.facultypage),
]
