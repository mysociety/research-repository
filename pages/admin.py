from django.contrib import admin

# tweak to taste - simple at the top and more custom below
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from pages import models


def construct_model_resource(passed_model):
    class LocalResource(ModelResource):
        class Meta:
            model = passed_model

    return LocalResource


def io_admin_register(passed_model):
    """
    filter that registers ImportExportModelAdmin and
    assigns them a blank model_resource
    """
    model_resource = construct_model_resource(passed_model)

    def inner(admin_cls):
        class ModelAdmin(admin_cls):
            resource_class = model_resource

        admin.site.register(passed_model, ModelAdmin)
        return ModelAdmin

    return inner


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
        super(ImportExportModelAdmin, self).save_model(request, obj, form, change)
        if "zip_archive" in form.changed_data:
            obj.unpack_archive()
