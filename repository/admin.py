from django.contrib import admin
from repository import models


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'institution')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

admin.site.register(models.Person, PersonAdmin)


class ItemAuthorInline(admin.TabularInline):
    model = models.ItemAuthor
    extra = 1


class ResearchOutputInline(admin.TabularInline):
    model = models.ResearchOutput


class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'friendly_date', 'author_list')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ItemAuthorInline, ResearchOutputInline)

admin.site.register(models.ResearchItem, ResearchItemAdmin)
