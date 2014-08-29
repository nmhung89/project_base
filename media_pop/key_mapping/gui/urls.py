from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('media_pop.key_mapping.gui.home.urls')),
)
