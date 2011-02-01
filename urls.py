from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^feed_reader_project/', include('feed_reader_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^lista_feeds/$', 'feed_reader_app.views.lista_feeds'),
    (r'^lista_feeds/(?P<selected_feader>\d+)/$', 'feed_reader_app.views.lista_feeds'),

    (r'^adiciona_feader/$', 'feed_reader_app.views.adiciona_feader'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}),
    (r'^refresh_feeds/$', 'feed_reader_app.views.refresh_feeds'),
    (r'^register/$', 'feed_reader_app.views.register'),
    (r'^remove_feader/(?P<selected_feader>\d+)/$', 'feed_reader_app.views.remove_feader'),
    (r'^remove_feed/(?P<selected_feed>\d+)/$', 'feed_reader_app.views.remove_feed'),
    (r'^restore_excl_feeds/$', 'feed_reader_app.views.restore_excl_feeds'),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
