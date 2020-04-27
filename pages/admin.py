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


@io_admin_register(models.OptOut)
class OptOutAdmin(ImportExportModelAdmin):
    pass


@io_admin_register(models.MiniSite)
class MiniSiteAdmin(ImportExportModelAdmin):
    pass

    def save_model(self, request, obj, form, change):

        super(ImportExportModelAdmin, self).save_model(
            request, obj, form, change)
        if 'zip_archive' in form.changed_data:
            obj.unpack_archive()
