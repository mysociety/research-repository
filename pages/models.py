from django.db import models


class Page(models.Model):

    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=200)

    slug = models.CharField(
        max_length=64,
        unique=True,
        help_text='Used to produce a nice URL for this page.'
    )

    content = models.TextField()

    def __unicode__(self):
        return self.title
