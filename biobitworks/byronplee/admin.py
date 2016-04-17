from django.contrib import admin
from .models import Person, Employer, Reference

class EmployerInline(admin.StackedInline):
    model = Employer
    extra = 3

class ReferenceInline(admin.StackedInline):
    model = Reference
    extra = 2

class PersonAdmin(admin.ModelAdmin):
    inlines = [EmployerInline]

class EmployerAdmin(admin.ModelAdmin):
    inlines = [ReferenceInline]

# Register your models here.

admin.site.register(Person, PersonAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Reference)



