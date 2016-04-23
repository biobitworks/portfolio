__author__ = 'byronlee'

from django.forms import ModelForm
from models import *
from django import forms

class PaperForm(ModelForm):
    class Meta:
        model = Paper


class AuthorshipForm(ModelForm):
    class Meta:
        model=Authorship

class PubMedIDForm(forms.Form):
     pubmed_id=forms.CharField(max_length=20)





