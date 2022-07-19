from unicodedata import category
from django.contrib import admin
from .models import Profile, Company, Employee


# Register your models here.
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Employee)

