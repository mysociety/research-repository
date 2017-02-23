from django.db import models
from autoslug import AutoSlugField
from markitup.fields import MarkupField


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = AutoSlugField(
        unique=True,
        editable=True,
        populate_from=('first_name', 'last_name'),
        help_text='Used to produce a nice page URL for this person\'s work.'
    )
    institution = models.CharField(
        max_length=50,
        help_text='The institution this person works for at time of publication.',
        blank=True
    )
    orcid = models.CharField(
        max_length=19,
        help_text='This person\'s ORCID iD (https://orcid.org/).',
        blank=True
    )
    researcherid = models.CharField(
        max_length=30,
        help_text='This person\'s ResearcherID (https://www.researcherid.com/).',
        blank=True
    )

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.full_name()


class ResearchItem(models.Model):

    class Meta:
        ordering = ['date']

    title = models.CharField(max_length=200)

    date = models.DateField()

    slug = AutoSlugField(
        unique=True,
        editable=True,
        populate_from=('title',),
        help_text='Used to produce a nice page URL for this item.'
    )

    authors = models.ManyToManyField(
        Person,
        through='ItemAuthor',
        help_text='Authors of this research item.'
    )

    abstract = MarkupField()

    funders = MarkupField(
        blank=True
    )

    LICENSE_CHOICES = (
        ('cc-by-3.0', 'Creative Commons Attribution 3.0 Unported License'),
    )

    license = models.CharField(
        max_length=16,
        choices=LICENSE_CHOICES
    )

    def author_list(self):
        return [authors.person for authors in ItemAuthor.objects.filter(research_item=self).order_by('order')]

    def friendly_date(self):
        return self.date.strftime("%B %Y")

    def licence_template_string(self):
        return 'licenses/' + self.licence + '.html'

    def __unicode__(self):
        return self.title + ' (' + self.friendly_date() + ')'


class ItemAuthor(models.Model):

    class Meta:
        ordering = ['order']

    person = models.ForeignKey(
        Person
    )
    research_item = models.ForeignKey(
        ResearchItem
    )
    order = models.IntegerField(
        verbose_name='Order',
        help_text='Where in the list of authors should this person appear?'
    )

    def __unicode__(self):
        return self.person.full_name() + ' is an author of "' + self.research_item.title + ('"" in position %d' % self.order)


class ResearchOutput(models.Model):

    title = models.CharField(max_length=200)

    research_item = models.ForeignKey(
        ResearchItem,
        related_name='outputs'
    )

    file = models.FileField(
        upload_to='outputs/',
        blank=True,
        help_text='If the output is a file we should host ourselves, upload it.'
    )

    url = models.URLField(
        blank=True,
        help_text='If the output is hosted elsewhere (like a journal), what is the URL?'
    )

    def __unicode__(self):
        return self.title
