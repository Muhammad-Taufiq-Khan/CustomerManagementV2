from django.contrib import admin
from .models import *
#import django
#from django.template.backends import django
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
