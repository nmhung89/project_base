from django.conf.urls import patterns, url

from my_company.my_app.gui.detail.views import DetailView, DetailAjaxView


urlpatterns = patterns('',
    url(r'^$', DetailView.as_view()),
    url(r'^json/(?P<action>.+?)/$', DetailAjaxView.as_view()),
)
