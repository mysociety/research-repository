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

def migrate_licence(self, request, queryset):
    for model in queryset:
        model.migrate_licence()

migrate_licence.short_description = 'Migrate licence'


@io_admin_register(models.ResearchItem)
class ResearchItemAdmin(ImportExportModelAdmin):
    list_display = ('title', 'friendly_date', 'author_list', 'published',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ItemAuthorInline, ResearchOutputInline)
    filter_horizontal = ('tags',)
    list_filter = ('tags', 'published', 'featured')
    actions = [migrate_licence]

    def save_model(self, request, obj, form, change):
        # if value of generate thumbnail has changed
        # update

        obj.fetch_toc(save=False)
        super(ImportExportModelAdmin, self).save_model(
            request, obj, form, change)
        if obj.generate_thumbnail and not obj.thumbnail:
            obj.generate_thumbnail_from_hero()
            obj.save()
        if 'zip_archive' in form.changed_data:
            obj.unpack_archive()




@io_admin_register(models.Tag)
class TagItemAdmin(ImportExportModelAdmin):

    def save_model(self, request, obj, form, change):
        # if value of generate thumbnail has changed
        # update
        super(ImportExportModelAdmin, self).save_model(
            request, obj, form, change)
        if obj.generate_thumbnail and not obj.thumbnail:
            obj.generate_thumbnail_from_hero()
            obj.save()


admin.site.register(models.TagGroup)
admin.site.register(models.Site)
admin.site.register(models.ResearchLicence)