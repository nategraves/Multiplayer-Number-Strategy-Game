from django.conf.urls.defaults import *

urlpatterns = patterns('gifts.views',
	url('^view/(?P<uuid>.*)/$', 'view', name='view'),
)