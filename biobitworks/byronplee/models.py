from django.db import models


# Create your models here.
class Person(models.Model):
    prefix_name = models.CharField('Preferred Prefix', max_length=200)
    first_name = models.CharField('First Name', max_length=200)
    middle_name = models.CharField('Middle Name', max_length=200)
    last_name = models.CharField('Last Name', max_length=200)
    suffix_name = models.CharField('Suffix', max_length=200)
    dob = models.DateTimeField('Date of Birth')
    about = models.TextField('About Me')
    def __str__(self):
        return self.first_name+' '+self.last_name

class Employer(models.Model):
    employee = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_hired = models.DateTimeField('Hired Date')
    date_last = models.DateTimeField('Last Day of Work')
    name_employer = models.CharField('Employer', max_length=200)
    website_employer = models.CharField('Employer  Website', max_length=200)
    def __str__(self):
        return self.name_employer

class Reference(models.Model):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    endorsement = models.CharField(max_length=200)
    def __str__(self):
        return self.name+' from '+self.employer.name_employer

