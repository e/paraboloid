from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'paraboloid.views.home', name='home'),
    # url(r'^paraboloid/', include('paraboloid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^paraboloid/((?P<f>[\d.]+)|)/((?P<xran>[\d.]+)|)/((?P<size>[\d.]+)|)/((?P<shape>(square|circle))|)/$', 'plot.views.home'),
    (r'^paraboloid/paraboloid.png/((?P<f>[\d.]+)|)/((?P<xran>[\d.]+)|)/((?P<size>[\d.]+)|)/((?P<shape>(square|circle))|)/((?P<download>download)/|)$', 'plot.views.pimage'),
    (r'^paraboloid/$', 'plot.views.home'),
    (r'^paraboloid/i18n/', include('django.conf.urls.i18n')),
)
