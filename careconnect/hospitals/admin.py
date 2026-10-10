from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'total_beds', 'total_doctors')
    search_fields = ('name', 'location')


from django.contrib import admin

# Register your models here.
