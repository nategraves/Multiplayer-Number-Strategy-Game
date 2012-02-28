from django.conf.urls.defaults import *

urlpatterns = patterns('index.views',
	url(r'^$', 'index'),
)