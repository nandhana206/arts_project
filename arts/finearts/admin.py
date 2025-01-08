from django.contrib import admin
from .models import Student
# Register your models here.

admin.site.register(Student)
#class StudentAdmin(admin.ModelAdmin):
 #   list_display = ('name', 'admission_number','department')
  #  search_fields = ('name', 'admission_number','department')