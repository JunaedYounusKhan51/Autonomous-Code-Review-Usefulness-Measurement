from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^upload/$', views.upload_code_review, name='upload_code_review'),
    url(r'^project/$', views.project, name='project'),
    url(r'^project/add/$', views.project_add, name='project_add'),
    url(r'^project/list/$', views.project_list, name='project_list'),
    url(r'^project/(?P<project_id>[0-9]+)$', views.project_detail, name='project_detail'),
    url(r'^project/delete/(?P<project_id>[0-9]+)$', views.project_delete, name='project_delete'),
    url(r'^project/update/$', views.project_update, name='project_update'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/commits/(?P<project_id>[0-9]+)/$', views.project_commits, name='project_commits'),
    url(r'^projects/reviews/(?P<commit_id>[0-9]+)/$', views.project_reviews, name='project_reviews'),    
    url(r'^projects/review/(?P<review_id>[0-9]+)/$', views.project_review_detail, name='project_review_detail'),
    url(r'^projects/review/update/$', views.project_review_update, name='project_review_update'),
    url(r'^usefulness/update/$', views.usefulness_update, name='usefulness_update'),
    url(r'^customize/$', views.customize, name='customize'),
    url(r'^customize/(?P<role_id>[0-9]+)$', views.customize_detail, name='customize_detail'),
    url(r'^customize/update/$', views.customize_update, name='customize_update'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/searchaction/$', views.searchaction, name='searchaction'),
    url(r'^report/$', views.report, name='report'),
    url(r'^report/projectwise/$', views.report_project, name='report_project'),
    url(r'^report/reviewerwise/$', views.report_reviewer, name='report_reviewer'),
    url(r'^report/yearwise/$', views.report_year, name='report_year'),
    url(r'^report/projectwisecreate/$', views.report_project_create, name='report_project_create'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/loginaction/$', views.loginaction, name='loginaction'),
]