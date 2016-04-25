from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()



urlpatterns = ['',
    url(r'^byronplee/', include('byronplee.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^labwebsite/', include('labwebsite.urls')),
]

