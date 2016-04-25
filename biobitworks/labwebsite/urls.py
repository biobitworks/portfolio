from django.conf.urls import patterns, url, include


from labwebsite import views


urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.home, name='home'),
    url(r'^index2/$', views.home2, name='home2'),
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^publications.html$', views.publications, name='publications'),
    url(r'^publications/(?P<paper_id>\d+)/$', views.article, name='article'),
    url(r'^people/$', views.people, name='people'),
    url(r'^people.html$', views.people, name='people'),
    # url(r'^alumni/$', views.alumni, name='alumni'),
    # url(r'^alumni.html$', views.alumni, name='alumni'),
    url(r'^people/(?P<labmember_id>\d+)/$', views.profile, name='profile'),
    url(r'^about/$', views.about, name='about'),
    url(r'^about.html$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact.html$', views.contact, name='contact'),
    url(r'^add_paper/$', views.add_paper, name='add_paper'),
    url(r'^edit_paper/(?P<paper_id>\d+)/$', views.edit_paper, name='edit_paper'),
    url(r'^add_paper_from_pubmed/$', views.add_paper_from_pubmed, name='add_paper_from_pubmed'),
    url(r'^social/$', views.social, name='social'),
    # url(r'^research/$', views.research, name='research'),
    # url(r'^research.html$', views.research, name='research'),
    (r'^social/', include('photologue_custom.urls')),
    (r'^social/', include('photologue.urls')),
    (r'^pages/', include('django.contrib.flatpages.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Your other patterns here
urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)