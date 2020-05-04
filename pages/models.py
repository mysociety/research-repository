import os
import zipfile
import shutil

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


class Page(models.Model):

    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=200)

    show_title = models.BooleanField(
        help_text='Should the template display the page title as well as the content?',
        default=True
    )

    slug = models.CharField(
        max_length=64,
        unique=True,
        help_text='Used to produce a nice URL for this page.'
    )

    content = models.TextField()

    nav_order = models.IntegerField(default=-1)

    social_image = models.ImageField(
        upload_to='social/',
        null=True,
        blank=True,
        editable=True,
        help_text="Image to be used on social shares of the site"
    )

    social_title = models.CharField(max_length=200, default="", null=True, blank=True)
    social_description = models.CharField(max_length=200, null=True, blank=True)
    social_big_image = models.BooleanField(default=False)

    def get_social_title(self):
        if self.social_title:
            return self.social_title
        else:
            return self.title

    def get_social_desc(self):
        if self.social_description:
            return self.social_description
        else:
            return self.title

    def __unicode__(self):
        return self.title


class Link(models.Model):

    label = models.CharField(max_length=200)
    url = models.URLField()
    order = models.IntegerField(default=-1)
    new_window = models.BooleanField(default=False)

    def __unicode__(self):
        return self.label


class OptOut(models.Model):
    """
    Used to record opt-outs from non-mailchimp surveys
    """
    experiment = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.user_id


class MiniSite(models.Model):
    """
    Model to manage upload of minisite zips
    """
    slug = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    site_folder = models.CharField(max_length=200)
    zip_archive = models.FileField(
        upload_to='zips/',
        blank=True,
        null=True,
        help_text='Upload a website as a zip',
        storage=OverwriteStorage()
    )
    last_update = models.DateTimeField(null=True, blank=True)

    def url(self):
        s = settings
        return s.SITE_BASE_URL + s.SITES_URL + self.site_folder + "/"

    def unpack_archive(self, preserve_existing=False):
        """
        extracts zip archive to destination directory
        """
        if not self.zip_archive:
            return None
        print ("unpacking zip")
        zip_location = self.zip_archive.path
        dest = os.path.join(settings.SITES_ROOT, self.site_folder)
        if os.path.exists(dest) and preserve_existing is False:
            shutil.rmtree(dest)
        zip_ref = zipfile.ZipFile(zip_location, 'r')
        zip_ref.extractall(dest)
        zip_ref.close()
        self.last_update = timezone.now()
        self.save()
