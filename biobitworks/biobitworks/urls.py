from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from biobitworks import settings


urlpatterns = ['',
    url(r'^byronplee/', include('byronplee.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^labwebsite/', include('labwebsite.urls')),
]


