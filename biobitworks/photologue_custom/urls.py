from django.conf.urls import *

from photologue.views import GalleryListView

urlpatterns = patterns('',
                       url(r'^gallery/page/(?P<page>[0-9]+)/$',
                           GalleryListView.as_view(paginate_by=5), name='pl-gallery-list'),
                       )