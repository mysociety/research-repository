from django.db import models
from autoslug import AutoSlugField
from markitup.fields import MarkupField
from django.conf import settings
from django.core import urlresolvers
from django.db.models import F
from django.utils.safestring import mark_safe
import urllib, json
from django.template import loader


class TagGroup(models.Model):
    slug = AutoSlugField(
        unique=True,
        editable=True,
        populate_from=('name')
    )

    name = models.CharField(max_length=30)

    hero = models.ImageField(
        upload_to='hero/',
        null=True,
        blank=True,
        editable=True,
        help_text="A hero image which will be displayed on this tag group's page. Recommended ratio is 1024x350."
    )

    description = MarkupField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    label = models.CharField(
        max_length=30,
        blank=True,
    )
    
    slug = models.SlugField(
        max_length=30,
        unique=True
    )

    hero = models.ImageField(
        upload_to='hero/',
        null=True,
        blank=True,
        editable=True,
        help_text="A hero image which will be displayed on this tag's page. Recommended ratio is 1024x350."
    )

    description = MarkupField(
        blank=True
    )

    tag_groups = models.ManyToManyField(TagGroup,blank=True,related_name="tags")
    
    display = models.BooleanField(default=True)
    
    top_bar = models.IntegerField(default=-1,
        help_text='Should this category appear on the top bar?'
    )

    display_items_in_years = models.BooleanField(default=True,
                            help_text='On the tag page - does it display items in years?'
                                                 )

    def __unicode__(self):
        return self.nice_name()

    def get_research_items(self):
        return self.items.all().filter(published=True).order_by('-date')

    def nice_name(self):
        if self.label:
            return self.label
        if "-" in self.slug:
            return self.slug.replace("-"," ").title()
        else:
            return self.slug.title()

    class Meta:
        ordering = ['slug']

class TagDisplayFilter(models.Model):
    """
    model to manage when secondary tags should be part of the tag navigation
    """
    parent = models.ForeignKey(Tag,related_name="display_filters")
    tag = models.ForeignKey(Tag)
    order = models.IntegerField(default=0)

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
    googlescholar = models.CharField(
        verbose_name='Google Scholar ID',
        max_length=30,
        help_text='This person\'s Google Scholar ID (https://scholar.google.com/).',
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
        blank=True,
        default=False
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
        default="none"
    )

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def absolute_url(self):
        return settings.SITE_BASE_URL + urlresolvers.reverse('person', args=[self.slug])

    def preferred_url(self):
        if self.link_behaviour == 'profile-page':
            return self.absolute_url()
        elif self.link_behaviour == 'url' and self.url:
            return self.url

    def json_ld_representation(self):

        json_ld_representation = {
                "@context": "http://schema.org",
                "@type": "Person",
                "familyName": self.last_name,
                "givenName": self.first_name,
                "name": self.full_name()
                }

        if self.institution:
            json_ld_representation['affiliation'] = {
                    "@type": "Organization",
                    "name": self.institution,
                }

        author_alternate_urls = []

        if self.preferred_url():
            json_ld_representation['url'] = self.preferred_url()
            author_alternate_urls.append(self.preferred_url())

        if self.url:
            author_alternate_urls.append(self.url)

        if self.absolute_url():
            author_alternate_urls.append(self.absolute_url())

        if self.orcid:
            author_alternate_urls.append('http://orcid.org/' + self.orcid)

        if self.googlescholar:
            author_alternate_urls.append('https://scholar.google.co.uk/citations?user=' + self.googlescholar)

        if self.researcherid:
            author_alternate_urls.append('http://www.researcherid.com/rid/' + self.researcherid)

        if self.twitter:
            author_alternate_urls.append('https://twitter.com/' + self.twitter)

        # This exciting line deduplicates the list.
        json_ld_representation['sameAs'] = list(set(author_alternate_urls))

        return json_ld_representation

    def items_list(self):
        return [items.research_item for items in ItemAuthor.objects.filter(person=self).order_by('-research_item__date')]

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

    published = models.BooleanField(
        help_text='Should this item be visible in listings, and indexable by search engines? Items will always be visible via their URL.'
    )

    featured = models.BooleanField(
        help_text='Should this item be featured on the homepage?',
        default=False
    )

    hero = models.ImageField(
        upload_to='hero/',
        null=True,
        blank=True,
        editable=True,
        help_text="A hero image which will be displayed on this research's page. Recommended ratio is 1024x680."
    )

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        editable=True,
        help_text="The thumbnail of this research. Recommended ratio is 150x110."
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
    
    show_citation = models.BooleanField(default=True)
    
    custom_cite = MarkupField(blank=True,default="")

    tags = models.ManyToManyField(Tag, blank=True,related_name="items")
    
    table_of_contents_url = models.URLField(blank=True,default="")
    table_of_contents_cache = models.TextField(blank=True,default="", editable=False)
    

    def fetch_toc(self,save=True):
        if self.table_of_contents_url:
            try:
                response = urllib.urlopen(self.table_of_contents_url)
                self.table_of_contents_cache = response.read()
            except Exception:
                pass
            if save:
                self.save()

    def json_toc(self):
        j = json.loads(self.table_of_contents_cache)
        for item in j:
            if "&amp;" in item["name"]:
                item["name"] = item["name"].replace("&amp;","&")
            for c in item["children"]:
                if "&amp;" in c["name"]:
                    c["name"] = c["name"].replace("&amp;","&")
        return j
        
    
    def rendered_toc(self):
        template = loader.get_template('parts/researchtoc.html')
        return template.render({'item':self})
        
    def rendered_abstract(self):
        """
        allows keywords to be specified in abstract and replaced by database
        values
        """
        abstract = self.abstract.rendered
        if "$TOC" in abstract:
            abstract = abstract.replace("<p>$TOC</p>",self.rendered_toc())
        return mark_safe(abstract)

    def visible_tags(self):
        return self.tags.filter(display=True)

    def ordered_outputs(self):
        return self.outputs.all().exclude(order=-1).order_by('order')

    def ordered_top_outputs(self):
        return self.outputs.all().exclude(top_order=-1).order_by('top_order')

    def author_list(self):
        return [authors.person for authors in ItemAuthor.objects.filter(research_item=self).order_by('order')]

    def friendly_date(self):
        return self.date.strftime("%B %Y")

    def licence_template_string(self):
        return 'licenses/' + self.licence + '.html'

    def absolute_url(self):
        return settings.SITE_BASE_URL + urlresolvers.reverse('item', args=[self.slug])

    def __unicode__(self):
        return self.title + ' (' + self.friendly_date() + ')'

    def share_abstract(self):
        """
        reduced version of abstract for sharing
        """
        if self.subtitle:
            text = self.subtitle
        else:
            text = self.abstract.raw

        text = text.replace("$TOC","")

        if len(text) > 140:
            text = text[:140-4] + "[..]"
        return text
    
    def similar_items(self,limit=2):
        """
        find similar based on overlapping number of tags
        """
        minimum_score = 2
        
        tags = list(self.tags.all())
        ids = set([x.id for x in tags])
        all_items = ResearchItem.objects.filter(tags__in=tags,published=True).exclude(id=self.id).prefetch_related('tags')
        all_items = all_items.distinct()
        all_items = list(all_items)
        
        for i in all_items:
            our_ids = set([x.id for x in i.tags.all()])
            i.overlap = len(ids.intersection(our_ids))
         
        all_items.sort(key=lambda x:x.date, reverse=True)   
        all_items.sort(key=lambda x:x.overlap, reverse=True)
        all_items = [x for x in all_items if x.overlap >= minimum_score]
            
            
        return all_items[:limit]
    
        
        

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

    download_count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    top_order = models.IntegerField(default=-1,
                                    help_text='Order for under image link')

    def increment_download(self):
        query = ResearchOutput.objects.filter(id=self.id)
        query.update(download_count=F('download_count') + 1)

    def button_url(self):
        if self.file:
            return self.file.url
        else:
            return self.url

    def button_text(self):
        if self.button_text_value:
            return self.button_text_value

        if self.file:
            return 'Download'

        else:
            return 'View Online'

    def __unicode__(self):
        return self.title


class Site(models.Model):
    """
    Holds site level information
    - should only have one entry
    """
    site_title = models.CharField(max_length=30,default="")
    default_tag = models.ForeignKey(Tag,null=True,blank=True)
    twitter = models.CharField(max_length=30,default="")
    description =  models.CharField(max_length=255,default="")
    
    
    @classmethod
    def get_default(cls):
        try:
            return cls.objects.all()[0]
        except Exception:
            s = Site()
            s.save()
            return s
    