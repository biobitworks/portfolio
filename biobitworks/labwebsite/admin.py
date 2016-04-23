from django.contrib import admin
from labwebsite.models import *

class FormerAffiliationsInline(admin.StackedInline):
    model=FormerAffiliations
    extra=0

class EducationInline(admin.StackedInline):
    model=Education
    extra=0

class ScientificInterestInline(admin.StackedInline):
    model=ScientificInterest
    extra=0

class SocialInline(admin.StackedInline):
    model = Social
    extra=0

class PersonInline(admin.StackedInline):
    model=Person
    extra=0

class CurrentWorkInline(admin.StackedInline):
    model = CurrentWork
    extra = 0

class OtherPublicationsInline(admin.StackedInline):
    model = OtherPublications
    extra = 0

class AuthorshipInline(admin.TabularInline):
    model = Authorship
    extra = 5

class LabMemberAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields':['person']}),
    # ]
    inlines = [SocialInline, CurrentWorkInline, OtherPublicationsInline, ScientificInterestInline, EducationInline, FormerAffiliationsInline]
    search_fields=['person__first_name', 'person__last_name']


class CommentaryInline(admin.StackedInline):
    model = Commentary
    extra = 0

class F1000Inline(admin.StackedInline):
    model = F1000
    extra = 0

class PaperAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['title', 'abstract']}),
        ('Date information', {'fields': ['pubdate']}),
        #('Authors', {'fields':['authors']}),
        ('Journal Info', {'fields':['journal', 'volume', 'page_start', 'page_end', 'pagination']}),
        ('Links', {'fields':['googlescholar', 'pubmed', 'DOI', 'publicationlink', 'pdf']}),
        ('Unique Publication IDs', {'fields':['PMID', 'eID']}),
    ]
    inlines = [AuthorshipInline, CommentaryInline, F1000Inline]
    list_filter=['pubdate']
    search_fields = ['title']

class LabMemberInline(admin.StackedInline):
    model=LabMember

class PersonAdmin(admin.ModelAdmin):
    inlines=[LabMemberInline]
    search_fields = ['first_name', 'middle_name', 'last_name']
    ordering = ['last_name']

class Research_Content_Admin(admin.ModelAdmin):
    model = Research_Content

class Research_Image_Admin(admin.ModelAdmin):
    model = Research_Image



admin.site.register(Address)
admin.site.register(Social)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Authorship)
admin.site.register(Person, PersonAdmin)
admin.site.register(LabMember, LabMemberAdmin)
admin.site.register(KVP)
admin.site.register(FormerAffiliations)
admin.site.register(Education)
admin.site.register(ScientificInterest)
admin.site.register(CurrentWork)
admin.site.register(OtherPublications)
admin.site.register(Commentary)
admin.site.register(F1000)
admin.site.register(Research_Content, Research_Content_Admin)
admin.site.register(Research_Image, Research_Image_Admin)
admin.site.register(Research_Summary)