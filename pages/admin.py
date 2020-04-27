from django.contrib import admin
from pages import models
# tweak to taste - simple at the top and more custom below
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource


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

# class FooBarAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["name"]}
#     list_display  = [ 'slug', 'name', ]
#     search_fields = ['name']
#
# admin.site.register( models.FooBar, FooBarAdmin )
