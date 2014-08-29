from django.conf.urls import patterns, url

from media_pop.key_mapping.gui.home.views import HomeView, HomeAjaxView


urlpatterns = patterns('',
    url(r'^json/(?P<action>.+?)/$', HomeAjaxView.as_view()),
    url(r'^$', HomeView.as_view()),
)
