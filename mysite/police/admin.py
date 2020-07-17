from django.contrib import admin
from .models import Cat, Crime, OffenseCat, Officer, Arrest, Case

# Register your models here.
admin.site.register(Cat)
admin.site.register(Crime)
admin.site.register(OffenseCat)
admin.site.register(Officer)
admin.site.register(Arrest)
admin.site.register(Case)