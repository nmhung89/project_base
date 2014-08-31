from django.conf.urls import patterns, url

from media_pop.key_mapping.gui.jqgrid.views import HomeJqgridAjaxView,\
    HomeJqgridView

urlpatterns = patterns('',
    url(r'^json/(?P<action>.+?)/$', HomeJqgridAjaxView.as_view()),
    url(r'^$', HomeJqgridView.as_view()),
)
