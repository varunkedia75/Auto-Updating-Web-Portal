from django.conf.urls import include, url
from django.contrib import admin
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^departments/', include('fpagecse.urls')),
    url(r'^$', views.homepage),
    url(r'login/$', views.login_user, name='login'),
    url(r'signup/$', views.register),
    url(r'login/basic_info$', views.basic_info  ),
    url(r'login/basic$', views.basic),
    url(r'login/teaching_page$', views.teaching_page),
    url(r'login/students_page$', views.students_page),
    url(r'login/students$', views.students),
    url(r'login/teaching$', views.teaching),
    url(r'login/publications_page$', views.publications_page),
    url(r'login/publication_crawler$', views.publication_crawler),
    url(r'login/teaching_crawler$', views.teaching_crawler),
    url(r'login/project_crawler$', views.project_crawler),
    url(r'login/publications$', views.publications),
    url(r'login/projects_page$', views.projects_page),
    url(r'login/projects$', views.projects),
    url(r'login/recognitions_page$', views.recognitions_page),
    url(r'login/recognitions$', views.recognitions),
    url(r'login/others_page$', views.others_page),
    url(r'login/others$', views.others),
    url(r'login/invitedtalks$', views.invitedtalks),
    url(r'login/responsibilities$', views.responsibilities),
    url(r'login/work$', views.work),
    url(r'login/education$', views.education),
    url(r'login/research$', views.research),
    url(r'logout$', views.logout_user),
    url(r'login/deletework$', views.deletework),
    url(r'login/deleteedu$', views.deleteedu),
    url(r'login/deleteinterest$', views.deleteinterest),
    url(r'login/deleteteaching$', views.deleteteaching),
    url(r'login/deleteprojects$', views.deleteprojects),
    url(r'login/deletepublication$', views.deletepublication),
    url(r'login/deleteothers$', views.deleteothers),
    url(r'login/deletestudents$', views.deletestudents),
    url(r'login/deleteinvitedtalks$', views.deleteinvitedtalks),
    url(r'login/deleterecognitions$', views.deleterecognition),
    url(r'login/mail_crawl$', views.mail_crawl),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^captcha/', include('captcha.urls')),
    ]
