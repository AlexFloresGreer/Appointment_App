from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^addappointment$', views.user),
    url(r'^appointments/(?P<task_id>\d+)$', views.edit, name = 'gohere'),
    url(r'^(?P<task_id>\d+)$', views.update),
    url(r'^delete/(?P<task_id>\d+)$', views.destroy),
]
