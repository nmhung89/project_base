from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', include('my_company.my_app.gui.home.urls'))
)
