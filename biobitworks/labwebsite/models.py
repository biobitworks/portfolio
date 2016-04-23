from django.db import models
from django.core.urlresolvers import reverse
from Bio import Entrez
from datetime import datetime
from biobitworks import settings

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    initials = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return '%s %s (%d)' % (self.first_name, self.last_name, self.id)

    class Meta:
        ordering = ('last_name', 'first_name',)

    @classmethod
    def get_by_first_initial_last_name_or_create(cls, first_name, last_name):
        people_that_match_last_name = Person.objects.filter(last_name=last_name)
        people_that_match = []
        for person in people_that_match_last_name:
            if person.first_name[0] == first_name[0]:
                people_that_match.append(person)

        author = None
        if len(people_that_match) == 0:
            author = Person(first_name=first_name, last_name=last_name)
            author.save()
        elif len(people_that_match) > 1:
            author = people_that_match[0]
        else:
            author = people_that_match[0]
        return author


    def is_lab_member(self):
        is_lab_member = False
        try:
            is_lab_member = self.labmember is not None
        except Exception:
            is_lab_member = False

        return is_lab_member
        #return LabMember.objects.filter(person=self).count() > 0

    def science_format(self):
        if self.is_lab_member():
            return self.labmember.science_format()
        else:
            return self.last_name + ' ' + self.first_name[0]


class LabMember(models.Model):
    person = models.OneToOneField(Person)
    summary = models.TextField('summary', blank=True)
    active = models.BooleanField()
    photo = models.ImageField(upload_to='photos', blank=True)
    email = models.EmailField('email', blank=True)
    position_title = models.CharField('position_title', max_length=200, blank=True)
    start_date = models.DateField('start_date', blank=True)
    pi=models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s' % (self.person.first_name, self.person.last_name)

    def science_format(self):
        profile_url = reverse("profile", kwargs={'labmember_id':self.id})
        person_string = self.person.last_name + ' ' + self.person.first_name[0]
        retval = "<a href='%s'>%s</a>" % (profile_url, person_string)
        return retval

# 	contact_email=models.EmailField('preferred email address', max_length=254)

class Paper(models.Model):
    title = models.TextField('title', blank=True)
    abstract = models.TextField('abstract', blank=True)
    pubdate = models.DateField('publication date', blank=True)
    journal = models.CharField('journal title', max_length=200, blank=True)
    #authorship
    authors = models.ManyToManyField(Person, through='Authorship')
    volume  =models.CharField('volume', max_length=200, blank=True)
    details = models.CharField('details', max_length=200, blank=True)
    pagination = models.CharField('pagination', max_length=200, blank=True)
    page_start = models.CharField('first page', max_length=10, blank=True)
    page_end = models.CharField('last page', max_length=10, blank=True)
    pdf = models.FileField(upload_to='paper', blank=True)
    googlescholar = models.URLField('link to google scholar', blank=True)
    pubmed = models.URLField('link to pubmed', blank=True)
    PMID = models.CharField('PMID', max_length=10, blank=True)
    DOI = models.CharField('DOI', max_length=200, blank=True)
    publicationlink = models.URLField('direct link to publication', blank=True)
    eID = models.CharField('eID', max_length=10, blank=True)
    # added commentaries
    # commentary = models.BooleanField(default=False)


    def __unicode__(self):
        return self.title

    def science_format_with_link(self):
        return self.science_format(should_include_link=True)

    def science_format_without_link(self):
        return self.science_format(should_include_link=False)


    def science_format(self, should_include_link):
        my_author_strings = []
        my_authorships = Authorship.objects.filter(paper_id=self.id).order_by('author_number')
        for my_authorship in my_authorships:
            person_for_authorship = my_authorship.person
            person_string_for_authorship = person_for_authorship.science_format()
            my_author_strings.append(person_string_for_authorship)
        authors_string = ", ".join(my_author_strings)

        title_string = None
        abstract_url_string = None
        pdf_link = None
        if should_include_link:
            paper_url = reverse("article", kwargs={'paper_id':self.id})
            title_string = '<a href="%s">%s</a>' % (paper_url, self.title)
            abstract_url_string = '<a href="%s">[Abstract]</a>' % (paper_url)
            pdf_link = '<a href="%s%s">[PDF]</a>' % (settings.MEDIA_URL, self.pdf)
        else:
            title_string='%s.' % (self.title)
            abstract_url_string = '[Abstract]'
            pdf_link = '[PDF]'

        retval = '<span class="author_list_link">%s.</span>  ' \
                 '<span class="pub_title_w_link">%s</span> ' \
                 '<span class="journal_title">%s</span> ' \
                 '<span class="pub_volume_name">%s</span>: ' \
                 '<span class="pub_volume_number">%s</span>, ' \
                 '<span class="pub_year">%s</span> ' \
                 '<br>' \
                 '<span type="button" class="btn-xs">%s</span> ' \
                 '<span type="button" class="btn-xs">%s</span> ' \
                 '<a ctype="button" class="btn-xs" href="http://www.ncbi.nlm.nih.gov/pubmed/%s">[PMID: %s]</a></span>' \
                 '<br><br>' \
                 % ( authors_string,
                     title_string,
                     self.journal,
                     self.volume,
                     self.pagination,
                     self.pubdate.year,
                     abstract_url_string,
                     pdf_link,
                     self.PMID,
                     self.PMID
        )
        print(science_format), retval.encode('UTF-8')
        return retval



class Authorship(models.Model):
    person = models.ForeignKey(Person)
    paper = models.ForeignKey(Paper)
    author_number = models.IntegerField('Author Number')

    def __unicode__(self):
        return '%s %s %s %s' % (self.person.last_name, self.person.first_name[0], self.paper.title, self.paper.pubdate)

class Commentary(models.Model):
    paper = models.ForeignKey(Paper)
    commentary_name = models.CharField('commentary_name', max_length=200, blank=True)
    commentary_link = models.URLField('commentary_link', blank=True)

class F1000(models.Model):
    paper = models.ForeignKey(Paper)
    F1000_name = models.CharField('F1000_name', max_length=200, blank=True)
    F1000_link = models.URLField('F1000_link', blank=True)


class Address(models.Model):
    lab_member = models.ForeignKey(LabMember)
    type = models.CharField('Current, Home, Mailing, etc.', max_length=200, blank=True)
    line1 = models.CharField('Address Line 1', max_length=200)
    line2 = models.CharField('Address Line 2', max_length=200, blank=True)
    city = models.CharField('City', max_length=30)
    state = models.CharField('City', max_length=2)
    country = models.CharField('Country', max_length=200)
    zip = models.CharField('Zip Code', max_length=5)

    def __unicode__(self):
        return '%s, %s - %s' % (self.lab_member.person.pylast_name, self.lab_member.person.first_name, self.type)


class Social(models.Model):
    lab_member = models.ForeignKey(LabMember)
    type = models.CharField('website name', max_length=200, blank=True)
    url = models.URLField('link to website', blank=True)

    def __unicode__(self):
        return '%s %s %s' % (self.lab_member.person.first_name, self.lab_member.person.last_name, self.type)

class FormerAffiliations(models.Model):
    lab_member = models.ForeignKey(LabMember)
    date_range = models.CharField('date_range', max_length=200, blank=True)
    position = models.CharField('position', max_length=200, blank=True)
    supervisor = models.CharField('supervisor', max_length=200, blank=True)
    institution = models.CharField('institution', max_length=200, blank=True)
    country = models.CharField('country', max_length=200, blank=True)

class Education(models.Model):
    lab_member = models.ForeignKey(LabMember)
    date_range = models.CharField('date_range', max_length=200, blank=True)
    degree_type = models.CharField('degree_type', max_length=200, blank=True)
    major = models.CharField('major', max_length=200, blank=True)
    institution = models.CharField('institution', max_length=200, blank=True)
    country = models.CharField('country', max_length=200, blank=True)

class ScientificInterest(models.Model):
    lab_member = models.ForeignKey(LabMember)
    interests = models.TextField('interests', blank=True)

class CurrentWork(models.Model):
    lab_member=models.ForeignKey(LabMember)
    current_work = models.TextField('current_work', blank=True)

class OtherPublications(models.Model):
    lab_member=models.ForeignKey(LabMember)
    list_of_publications = models.TextField('list_of_publications', blank=True)

class KVP(models.Model):
    key=models.CharField(max_length=200, blank=True)
    value=models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.key

def add_paper_from_pmid(pmid):
    default = ""
    Entrez.email="info@walterlab.ucsf.edu"
    handle = Entrez.efetch(db="pubmed", id=[pmid], rettype="XML", retmode="xml")
    record = Entrez.read(handle)
    #[i['LastName'] for i in record[0]['MedlineCitation']['InvestigatorList'] ]
    #pmid=str(records[0][u'MedlineCitation'][u'PMID'])
    pmid_article = record[0][u'MedlineCitation'][u'Article']
    title = unicode(pmid_article[u'ArticleTitle'])
    abstract = u''
    if u'Abstract' in pmid_article:
        abstract = unicode(pmid_article[u'Abstract'][u'AbstractText'][0])
    pmid_article_pubdate = pmid_article[u'Journal'][u'JournalIssue'][u'PubDate']
    if len(pmid_article[u'ArticleDate'])>0:
        pubday = pmid_article[u'ArticleDate'][0][u'Day']
        pubmonth = pmid_article[u'ArticleDate'][0][u'Month']
        pubyear = pmid_article[u'ArticleDate'][0][u'Year']
        pubdate = datetime.strptime(pubyear+'-'+pubmonth+'-'+pubday, "%Y-%m-%d")
    elif len(pmid_article_pubdate)==3:
        pubday=pmid_article_pubdate[u'Day']
        pubmonth=pmid_article_pubdate[u'Month']
        pubyear=pmid_article_pubdate[u'Year']
        pubdate = datetime.strptime(pubyear+'-'+pubmonth+'-'+pubday, "%Y-%b-%d")
    else:
        pubday = '01'
        pubmonth = 'Jan'
        pubyear = pmid_article_pubdate[u'Year']
        pubdate = datetime.strptime(pubyear+'-'+pubmonth+'-'+pubday, "%Y-%b-%d")

    journal = pmid_article[u'Journal'][u'ISOAbbreviation']
    volume = pmid_article[u'Journal'][u'JournalIssue'][u'Volume']
    # if len(pmid_article[u'ELocationID'][0])>0:
    #     doi = pmid_article[u'ELocationID'][0]
    # else:
    #     doi = ' '
    pagination = pmid_article[u'Pagination'][u'MedlinePgn']
    paper = Paper(
        PMID=pmid,
        title=title,
        abstract=abstract,
        journal=journal,
        pubdate=pubdate,
        volume=volume,
        #DOI=doi,
        pagination=pagination,
        )
    # paper=Paper(title=form.cleaned_data['pubmed_id'], pubdate="2012-01-01")
    paper.save()

    pmid_authors = record[0]['MedlineCitation'][u'Article']['AuthorList']
    author_number = 0
    for pmid_author in pmid_authors:
        author_number += 1
        last_name=unicode(pmid_author[u'LastName'])
        first_name=unicode(pmid_author[u'ForeName'])
        #initials=record[0]['MedlineCitation'][u'Article']['AuthorList'][x][u'Initials']
        #name=first_name+" "+last_name
        author = Person.get_by_first_initial_last_name_or_create(last_name=last_name, first_name=first_name)
        authorship = Authorship(person=author, paper=paper, author_number=author_number)
        authorship.save()

    return paper

class Research_Content(models.Model):
    topic_content_summary = models.CharField(max_length=255, blank=True)
    topic_content = models.TextField('topic_content', blank=True)
    content_number = models.CharField(max_length=3, blank=True)

    def __unicode__(self):
        return self.topic_content_summary

class Research_Image(models.Model):
    topic_image_tag = models.CharField(max_length=255, blank=True)
    topic_image = models.ImageField(upload_to='research_page_images', blank=True)
    image_number = models.CharField(max_length=3, blank=True)

    def __unicode__(self):
        return self.topic_image_tag

class Research_Summary(models.Model):
    heading = models.TextField('heading', blank=True)
    content = models.ForeignKey(Research_Content, blank=True)
    image = models.ForeignKey(Research_Image, blank=True)
    research_summary_number = models.CharField(max_length=3, blank=True)

    def __unicode__(self):
        return self.heading
