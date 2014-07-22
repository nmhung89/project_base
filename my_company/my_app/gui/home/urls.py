from django.conf.urls import patterns, url

from my_company.my_app.gui.home.views import HomeView, HomeAjaxView


urlpatterns = patterns('',
    url(r'^json/(?P<action>.+?)/$', HomeAjaxView.as_view()),
    url(r'^$', HomeView.as_view()),
)
