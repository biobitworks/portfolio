from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect

#from django.http import HttpResponse
#from django.core.urlresolvers import reverse

from .forms import *
from Bio import Medline
from Bio import Entrez

#Views

def home(request):
    context = {}
    return render(request, 'labapp/index.html', context)

def home2(request):
    context = {}
    return render(request, 'labapp/index2.html', context)

def about(request):
    context = {}
    context['about_active']='class=active'
    return render(request, 'labapp/about.html', context)

def index(request):
    context = {}
    return render(request, 'labapp/index.html', context)

def social(request):
    context = {}
    context['social_active']='class=active'
    return render(request, 'labapp/social.html', context)

#Publications

def publications(request):
    publications_list=Paper.objects.all().order_by('-pubdate')
    print(publications_list)
    context = {}
    context['publications']=publications_list
    context['publications_active']='class=active'
    return render(request, 'labapp/publications.html', context)

def article(request, paper_id):
    context={}
    myarticle=get_object_or_404(Paper, pk=paper_id)
    context['article']=myarticle
    authorships = Authorship.objects.filter(paper_id=paper_id).order_by('author_number')
    context['authorships'] = authorships

    commentary = Commentary.objects.filter(paper_id=paper_id)
    context['commentary'] = commentary

    f1000 = F1000.objects.filter(paper_id=paper_id)
    context['f1000'] = f1000

    return render (request, 'labapp/paper.html', context)

#People

def people(request):
    lab_members_list=LabMember.objects.filter(active=True).order_by('-pi', 'person__last_name')
    print(lab_members_list)

    context = {}
    context['lab_members_list'] = lab_members_list
    context['people_active']='class=active'

    return render(request, 'labapp/people.html', context)

def alumni(request):
    alumni_list=LabMember.objects.filter(active=False).order_by('person__last_name')
    print(alumni_list)

    context = {}
    context['alumni_list'] = alumni_list
    context['alumni_active']='class=active'

    return render(request, 'labapp/alumni.html', context)

def profile(request, labmember_id):
    context = {}

    mylabmember=get_object_or_404(LabMember, pk=labmember_id)
    context['labmember']=mylabmember

    affiliations = FormerAffiliations.objects.filter(lab_member_id=labmember_id)
    context['affiliations'] = affiliations

    education = Education.objects.filter(lab_member_id=labmember_id)
    context['education'] = education

    scientific_interest = ScientificInterest.objects.filter(lab_member_id=labmember_id)
    context['scientific_interest'] = scientific_interest

    social_networks = Social.objects.filter(lab_member_id=labmember_id)
    context['social_networks'] = social_networks

    current_work = CurrentWork.objects.filter(lab_member_id=labmember_id)
    context['current_work'] = current_work

    other_publications = OtherPublications.objects.filter(lab_member_id=labmember_id)
    context['other_publications'] = other_publications

    authorships=Authorship.objects.filter(person_id=mylabmember.person.id).order_by('-paper__pubdate')

    paper_list=[]
    for authorship in authorships:
        paper_list.append(authorship.paper)

    context["person_papers"]=paper_list



    return render(request, 'labapp/profile.html', context)

def contact(request):
    context = {}
    context['contact_active']='class=active'
    return render(request, 'labapp/contact.html', context)

def add_paper_from_pubmed(request):
    context = {}
    if request.POST:
        form = PubMedIDForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            pmid = form.cleaned_data['pubmed_id']
            paper = add_paper_from_pmid(pmid)
            return redirect("edit_paper", paper_id=paper.id)
        else:
            pass
    else:
        form = PubMedIDForm()

    context['form'] = form
    return render(request, 'labapp/add_paper.html', context)

def add_paper(request):
    context = {}

    if request.POST:
        form = PaperForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.save()
            for person in form.cleaned_data['authors']:
                authorship=Authorship()
                authorship.paper=paper
                authorship.person=person
                authorship.author_number = 99
                authorship.save()
            # paper.save()
            return redirect("publications")

        else:
            pass
    else:
        form = PaperForm()

    context['form'] = form
    return render(request, 'labapp/add_paper.html', context)

def edit_paper(request, paper_id):
    context = {}
    paper = Paper.objects.get(pk=paper_id)
    if request.POST:
        form = PaperForm(instance=paper, data=request.POST, files=request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.save()
            for person in form.cleaned_data['authors']:
                authorship=Authorship()
                authorship.paper=paper
                authorship.person=person
                authorship.save()
            # paper.save()
            return redirect("publications")

        else:
            pass
    else:
        form = PaperForm(instance=paper)


    context['form'] = form
    return render(request, 'labapp/edit_paper.html', context)

# def research(request):
#     context = {}
#     summaries = Research_Summary.objects.order_by('research_summary_number')
#     context['research_list'] = summaries
#     return render(request, 'labapp/research.html', context)



