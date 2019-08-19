from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^create_message$', views.create_message),
    url(r'^create_comment$', views.create_comment)
]
