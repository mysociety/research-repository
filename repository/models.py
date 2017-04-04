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
        help_text='The institution this person works for.',
        blank=True
    )
    orcid = models.CharField(
        verbose_name='ORCID ID',
        max_length=19,
        help_text='This person\'s ORCID ID (https://orcid.org/).',
        blank=True
    )
    researcherid = models.CharField(
        verbose_name='ResearcherID',
        max_length=30,
        help_text='This person\'s ResearcherID (https://www.researcherid.com/).',
        blank=True
    )
    twitter = models.CharField(
        max_length=50,
        help_text='This person\'s Twitter handle.',
        blank=True
    )
    url = models.URLField(
        help_text='A URL with more information on this person (such as an institutional URL).',
        blank=True
    )
    list_in_people = models.BooleanField(
        help_text='Should this person be included in the list of people?',
        blank=True
    )

    LINK_BEHAVIOUR_CHOICES = (
        ('profile-page', 'A profile page on research.mysociety.org'),
        ('url', 'Directly to the person\'s own URL (if known)'),
        ('none', 'Do not link this name'),
    )

    link_behaviour = models.CharField(
        max_length=16,
        choices=LINK_BEHAVIOUR_CHOICES,
        help_text='How should we link this person\'s name when given as an author?',
    )

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.full_name()

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'people'


class ResearchItem(models.Model):

    class Meta:
        ordering = ['-date']

    title = models.CharField(max_length=500)
    subtitle = models.CharField(
        max_length=1000,
        blank=True
    )

    date = models.DateField(
        help_text='The publication date of this item.'
    )

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

    LICENCE_CHOICES = (
        ('cc-by-3.0', 'Creative Commons Attribution 3.0 Unported License'),
    )

    licence = models.CharField(
        max_length=16,
        choices=LICENCE_CHOICES,
        blank=True
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

    button_text_value = models.CharField(
        max_length=200,
        blank=True,
        help_text='Optional custom text for the button to get this output.'
    )

    def button_url(self):
        if self.file:
            return self.file.url
        else:
            return self.url

    def button_text(self):
        if self.button_text_value:
            return self.button_text_value

        if self.file:
            return 'Download File'

        else:
            return 'Visit Website'

    def __unicode__(self):
        return self.title
