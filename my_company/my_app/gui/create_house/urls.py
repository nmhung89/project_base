from django.conf.urls import patterns, url

from my_company.my_app.gui.create_house.views import CreateHouseView,\
    CreateHouseAjaxView


urlpatterns = patterns('',
    url(r'^$', CreateHouseView.as_view()),
    url(r'^json/(?P<action>.+?)/$', CreateHouseAjaxView.as_view()),
)
