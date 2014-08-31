from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^jqgrid/', include('media_pop.key_mapping.gui.jqgrid.urls')),
    url(r'^', include('media_pop.key_mapping.gui.home.urls')),
)
