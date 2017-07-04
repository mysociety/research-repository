from django.contrib import admin
from repository import models
from import_export.admin import ImportExportModelAdmin 
from useful_inkleby.useful_django.admin import io_admin_register

@io_admin_register(models.Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'institution')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


class ItemAuthorInline(admin.TabularInline):
    model = models.ItemAuthor
    extra = 1

class ResearchOutputInline(admin.TabularInline):
    model = models.ResearchOutput

@io_admin_register(models.ResearchItem)
class ResearchItemAdmin(ImportExportModelAdmin):
    list_display = ('title', 'friendly_date', 'author_list')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ItemAuthorInline, ResearchOutputInline)
