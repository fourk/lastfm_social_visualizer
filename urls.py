from django.conf.urls.defaults import *
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
					(r'^site_media/(?P<path>.*)$', 
						'django.views.static.serve', 
						{'document_root': 'media'}),
						(r'^$', 'lfm.views.foo'),
						(r'^user/', 'lfm.views.get_top100'),
						(r'^youtube/(?P<id>.*?)/$', 'lfm.views.youtube'),
						(r'^playlists/load/$', 'lfm.views.playlist_list'),
						(r'^playlists/load/(?P<id>)$', 'lfm.views.playlist_load'),
						(r'^playlists/save/$', 'lfm.views.playlist_save'),
                        (r'^node/$', 'lfm.views.node_fwd'),
    # Example:
    # (r'^pylist/', include('pylist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
