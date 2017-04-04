from django.db import models


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

    def __unicode__(self):
        return self.title
