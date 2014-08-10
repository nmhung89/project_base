from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^detail/(?P<pk>.+?)/', include('my_company.my_app.gui.detail.urls')),
    url(r'^submit-property/', include('my_company.my_app.gui.create_house.urls')),
    url(r'^', include('my_company.my_app.gui.home.urls')),
)
