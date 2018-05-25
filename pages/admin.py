from django.contrib import admin
from pages import models
# tweak to taste - simple at the top and more custom below
from import_export.admin import ImportExportModelAdmin 
from useful_inkleby.useful_django.admin import io_admin_register


@io_admin_register(models.Page)
class PageAdmin(ImportExportModelAdmin):
    pass

@io_admin_register(models.Link)
class LinkAdmin(ImportExportModelAdmin):
    pass


# class FooBarAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["name"]}
#     list_display  = [ 'slug', 'name', ]
#     search_fields = ['name']
#
# admin.site.register( models.FooBar, FooBarAdmin )
