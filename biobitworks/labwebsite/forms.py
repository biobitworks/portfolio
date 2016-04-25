__author__ = 'byronlee'

from django.forms import ModelForm
from .models import *
from django import forms

class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = "__all__"


class AuthorshipForm(ModelForm):
    class Meta:
        model = Authorship
        fields = "__all__"

class PubMedIDForm(forms.Form):
     pubmed_id=forms.CharField(max_length=20)





