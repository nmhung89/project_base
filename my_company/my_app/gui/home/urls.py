from django.conf.urls import patterns, include, url
from my_company.my_app.gui.home.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view())
)
