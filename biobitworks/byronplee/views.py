from django.shortcuts import render

# Create your views here.
from .models import Person, Employer, Reference

def index(request):
    person_profile = Person.objects.get(pk=1)
    context = {'person_profile': person_profile}
    return render(request, 'index.html', context)

def employers(request):
    employee_x = Person.object.get(pk=1)
    employers_all = Employer.objects.all(employee_x)
    employers_list = list(employers_all)
    print(employers_list)
    context = {}
    context['employers_list'] = 'employers_list'
    return render(request, 'profile.html', context)

# def profile(request, person_id):
#     person_profile = Person.objects.get(pk=person_id)
#     context = {'person_profile': person_profile}
#     return render(request, 'profile.html', context)


