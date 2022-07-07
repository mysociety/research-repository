import json
import os
import shutil
from datetime import datetime
import zipfile
from typing import List

from autoslug import AutoSlugField
from django.conf import settings
from django.urls import reverse
from django.db.models import F, Q
from django.utils.safestring import mark_safe
import urllib.request, urllib.parse, urllib.error
import json
from django.template import loader
from django.core.files.base import ContentFile
from .image_processor import ThumbNailCreator
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import F, Q
from django.template import loader
from django.utils.safestring import mark_safe
from markdown import markdown
from markitup.fields import MarkupField

GENERATE_CHOICES = [
    ("B", "Blog"),
    ("R", "Report"),
    ("P", "Policy"),
    ("C", "Consultation"),
    ("M", "Minisite"),
    ("S", "Series"),
]


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


class ThumbnailMixIn(object):
    """
    mixin for tags and researchitems to generate thumbnails
    """

    def clean(self):
        if self.generate_thumbnail and not self.hero:
            raise ValidationError(
                "Trying to generate a thumbnail, but no hero uplaoded."
            )

    def generate_thumbnail_from_hero(self):
        """
        generate thumbnail from hero image
        """
        if not self.generate_thumbnail and self.hero:
            return None

        hero_path = self.hero.path
        tc = ThumbNailCreator()
        tcf = tc.convert_hero_image_to_thumbnail

        tempfile = tcf(hero_path, text=self.generate_thumbnail)

        cf = ContentFile(tempfile.getvalue())
        filename = "{0}-{1}.png".format(self.slug, "thumbnail")
        self.thumbnail.save(filename, cf, save=True)


class ResearchLicence(models.Model):
    """
    How is the research itself licenced
    """

    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    description = MarkupField(blank=True)

    def __str__(self):
        return self.slug

    def __str__(self):
        return self.slug


class TagGroup(models.Model):
    slug = AutoSlugField(unique=True, editable=True, populate_from=("name"))

    name = models.CharField(max_length=30)

    hero = models.ImageField(
        upload_to="hero/",
        null=True,
        blank=True,
        editable=True,
        help_text="A hero image which will be displayed on this tag group's page. Recommended ratio is 1024x350.",
    )

    description = MarkupField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Tag(models.Model, ThumbnailMixIn):
    label = models.CharField(
        max_length=30,
        blank=True,
    )

    slug = AutoSlugField(
        unique=True,
        editable=True,
        populate_from=("label",),
        help_text="Used to produce a nice page URL for this item.",
    )

    featured = models.BooleanField(default=False)
    date = models.DateField(
        help_text="The publication date of this tag.", null=True, blank=True
    )

    hero = models.ImageField(
        upload_to="hero/",
        null=True,
        blank=True,
        editable=True,
        help_text="A hero image which will be displayed on this tag's page. Recommended ratio is 1024x350.",
    )

    generate_thumbnail = models.CharField(
        choices=GENERATE_CHOICES,
        max_length=2,
        null=True,
        blank=True,
        editable=True,
        help_text="Generate a thumbnail from the hero image",
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        null=True,
        blank=True,
        editable=True,
        help_text="The thumbnail of this research. Recommended ratio is 150x110.",
    )

    description = MarkupField(blank=True)

    tag_groups = models.ManyToManyField(TagGroup, blank=True, related_name="tags")

    display = models.BooleanField(default=True)

    is_project = models.BooleanField(
        default=False, help_text="creates the 'part of' message in all members"
    )

    top_bar = models.IntegerField(
        default=-1, help_text="Should this category appear on the top bar?"
    )

    display_items_in_years = models.BooleanField(
        default=True, help_text="On the tag page - does it display items in years?"
    )

    social_description = models.CharField(max_length=255, null=True, blank=True)

    def get_social_description(self):
        if self.social_description:
            return self.social_description
        else:
            abstract = self.description.raw
            if len(abstract) > 250:
                return abstract[:250] + "[...]"
            else:
                return abstract

    def json(self):
        """
        return a json version of tag for export
        """

        def url_if_exists(v):
            if v:
                return settings.SITE_BASE_URL + v.url
            else:
                return ""

        di = {
            "title": self.title,
            "subtitle": "",
            "slug": self.slug,
            "date": self.date.isoformat(),
            "thumbnail": url_if_exists(self.thumbnail),
            "hero_image": url_if_exists(self.hero),
            "url": self.absolute_url(),
            "desc": self.get_social_description(),
        }
        di["authors"] = []
        return di

    def absolute_url(self):
        return settings.SITE_BASE_URL + reverse("tag", args=[self.slug])

    @property
    def title(self):
        return self.label

    def friendly_date(self):
        if self.date:
            return self.date.strftime("%B %Y")
        else:
            return ""

    def __str__(self):
        return self.nice_name()

    def get_research_items(self):
        return self.items.all().filter(published=True).order_by("-date")

    def count(self):
        return self.get_research_items().count()

    def nice_name(self):
        if self.label:
            return self.label
        if "-" in self.slug:
            return self.slug.replace("-", " ").title()
        else:
            return self.slug.title()

    def url(self):
        return reverse("tag", args=[self.slug])

    class Meta:
        ordering = ["slug"]


class TagDisplayFilter(models.Model):
    """
    model to manage when secondary tags should be part of the tag navigation
    """

    parent = models.ForeignKey(
        Tag, related_name="display_filters", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = AutoSlugField(
        unique=True,
        editable=True,
        populate_from=("first_name", "last_name"),
        help_text="Used to produce a nice page URL for this person's work.",
    )
    institution = models.CharField(
        max_length=50, help_text="The institution this person works for.", blank=True
    )
    orcid = models.CharField(
        verbose_name="ORCID ID",
        max_length=19,
        help_text="This person's ORCID ID (https://orcid.org/).",
        blank=True,
    )
    researcherid = models.CharField(
        verbose_name="ResearcherID",
        max_length=30,
        help_text="This person's ResearcherID (https://www.researcherid.com/).",
        blank=True,
    )
    googlescholar = models.CharField(
        verbose_name="Google Scholar ID",
        max_length=30,
        help_text="This person's Google Scholar ID (https://scholar.google.com/).",
        blank=True,
    )
    twitter = models.CharField(
        max_length=50, help_text="This person's Twitter handle.", blank=True
    )
    url = models.URLField(
        help_text="A URL with more information on this person (such as an institutional URL).",
        blank=True,
    )
    list_in_people = models.BooleanField(
        help_text="Should this person be included in the list of people?",
        blank=True,
        default=False,
    )

    LINK_BEHAVIOUR_CHOICES = (
        ("profile-page", "A profile page on research.mysociety.org"),
        ("url", "Directly to the person's own URL (if known)"),
        ("none", "Do not link this name"),
    )

    link_behaviour = models.CharField(
        max_length=16,
        choices=LINK_BEHAVIOUR_CHOICES,
        help_text="How should we link this person's name when given as an author?",
        default="none",
    )

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def absolute_url(self):
        return settings.SITE_BASE_URL + reverse('person', args=[self.slug])

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
            author_alternate_urls.append(
                'https://scholar.google.co.uk/citations?user=' + self.googlescholar)

        if self.researcherid:
            author_alternate_urls.append(
                'http://www.researcherid.com/rid/' + self.researcherid)

        if self.twitter:
            author_alternate_urls.append('https://twitter.com/' + self.twitter)

        # This exciting line deduplicates the list.
        json_ld_representation['sameAs'] = list(set(author_alternate_urls))

        return json_ld_representation

    def items_list(self):
        return [items.research_item for items in ItemAuthor.objects.filter(person=self).order_by('-research_item__date')]

    def __str__(self):
        return self.full_name()

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'people'


class ResearchItem(models.Model, ThumbnailMixIn):

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

    generate_thumbnail = models.CharField(
        choices=GENERATE_CHOICES,
        max_length=2,
        null=True,
        blank=True,
        editable=True,
        help_text="Generate a thumbnail from the hero image"
    )

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        editable=True,
        help_text="The thumbnail of this research. Recommended ratio is 150x110."
    )

    social_large = models.ImageField(
        upload_to='social/',
        null=True,
        blank=True,
        editable=True,
        help_text="The thumbnail of this research. Recommended ratio is 1200*630"
    )

    authors = models.ManyToManyField(
        Person,
        through='ItemAuthor',
        help_text='Authors of this research item.'
    )

    abstract = MarkupField()

    social_description = models.CharField(max_length=255,
                                          null=True,
                                          blank=True)

    funders = MarkupField(
        blank=True
    )

    LICENCE_CHOICES = (
        ('cc-by-3.0', 'Creative Commons Attribution 3.0 Unported License'),
        ('pub-rights', 'Publication rights only'),
    )

    licence = models.CharField(
        max_length=16,
        choices=LICENCE_CHOICES,
        blank=True,
        help_text="Deprecated, use 'licencing'."
    )

    licencing = models.ForeignKey(ResearchLicence, null=True, blank=True, on_delete=models.CASCADE)

    show_citation = models.BooleanField(default=True)
    show_disclaimer = models.BooleanField(default=False,
                                          help_text='Shows external author disclaimer.')

    custom_cite = MarkupField(blank=True, default="",
                              help_text='Replaces the automatically generate citation with a manual one.')

    tags = models.ManyToManyField(Tag, blank=True, related_name="items")

    table_of_contents_url = models.URLField(blank=True, default="",
                                            help_text='External .json to create TOC')
    table_of_contents_cache = models.TextField(
        blank=True, default="", editable=True,
        help_text='Stores retrieved json site stucture - can also be used as a markdown field for the contents list')

    photo_credit = MarkupField(blank=True, default="",
                               help_text='Photo credit for image')

    zip_archive = models.FileField(
        upload_to='zips/',
        blank=True,
        null=True,
        help_text='Upload a stringprint document as a zip',
        storage=OverwriteStorage()
    )

    def migrate_licence(self):
        """
        migrate from old style to new style licences
        """
        name_lookup = {x: y for x, y in ResearchItem.LICENCE_CHOICES}
        if self.licencing is None and self.licence:
            replacement, created = ResearchLicence.objects.get_or_create(
                slug=self.licence, name=name_lookup[self.licence])
            self.licencing = replacement
            self.save()

    def special_urls(self):
        """
        find and return urls for some formats of the page
        mainly for crawlers benefit.
        """
        results = {}

        options = {"pdf": ["pdf"],
                   "full_text": ["read online", "mysociety blog"]
                   }

        for k, v in options.items():
            query = Q()
            for phrase in v:
                query |= Q(title__icontains=phrase)

            outputs = self.outputs.filter(query)
            if outputs.exists():
                option = outputs[0]
                results[k] = option

        return results

    def url(self):
        return reverse('item', args=[self.slug])

    def has_thumbnail(self):
        if self.thumbnail:
            return True
        return False

    def get_social_description(self):
        if self.social_description:
            return self.social_description
        else:
            abstract = self.abstract.raw
            if len(abstract) > 250:
                return abstract[:250] + "[...]"
            else:
                return abstract

    def json(self):
        """
        return a json version of item for export
        """

        def url_if_exists(v):
            if v:
                return settings.SITE_BASE_URL + v.url
            else:
                return ""

        di = {
            "title": self.title,
            "subtitle": self.subtitle,
            "slug": self.slug,
            "date": self.date.isoformat(),
            "thumbnail": url_if_exists(self.thumbnail),
            "hero_image": url_if_exists(self.hero),
            "url": self.absolute_url(),
            "desc": self.get_social_description(),
        }
        authors = self.authors.all()
        di["authors"] = [x.json_ld_representation() for x in authors]
        return di

    def projects(self):
        return self.tags.filter(is_project=True)

    def unpack_archive(self):
        """
        extracts zip archive to holding directory
        """
        if not self.zip_archive:
            return None
        zip_location = self.zip_archive.path
        upload_name = os.path.split(zip_location)[1]
        upload_slug = os.path.splitext(upload_name)[0]
        dest = os.path.join(settings.ZIP_ROOT, upload_slug)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        url_path = settings.SITE_BASE_URL + settings.ZIP_URL + upload_slug + "/"
        zip_ref = zipfile.ZipFile(zip_location, 'r')
        zip_ref.extractall(dest)
        zip_ref.close()

        # connect outputs if not already present
        gc = ResearchOutput.objects.get_or_create
        current_urls = list(self.outputs.all().values_list("url", flat=True))

        if os.path.exists(os.path.join(dest, "toc.json")):
            self.table_of_contents_url = url_path + "toc.json"
            self.fetch_toc(save=True)
        url = url_path
        if os.path.join(dest, "index.html") and url not in current_urls:
            item, created = gc(title="Read Online", research_item=self)
            item.url = url
            item.order = 0
            item.top_order = 0
            item.save()
        url = url_path + "plain.html"
        if os.path.exists(os.path.join(dest, "plain.html")) and url not in current_urls:
            item, created = gc(title="Plain Text", research_item=self)
            item.url = url
            item.order = 1
            item.top_order = 1
            item.save()
        kindle_file = "{0}.mobi".format(upload_slug)
        url = url_path + kindle_file
        if os.path.exists(os.path.join(dest, kindle_file)) and url not in current_urls:
            item, created = gc(title="Kindle .mobi", research_item=self)
            item.url = url
            item.order = 2
            item.top_order = 2
            item.save()
        epub_file = "{0}.epub".format(upload_slug)
        url_path + kindle_file
        if os.path.exists(os.path.join(dest, epub_file)) and url not in current_urls:
            item, created = gc(title="epub", research_item=self)
            item.url = url
            item.order = 2
            item.top_order = 2
            item.save()
        self.save()

    def fetch_toc(self, save=True):
        if self.table_of_contents_url:
            try:
                response = urllib.request.urlopen(self.table_of_contents_url)
                self.table_of_contents_cache = response.read().decode("utf-8")
            except Exception:
                pass
            if save:
                self.save()

    def is_json_toc(self):
        try:
            j = json.loads(self.table_of_contents_cache)
        except ValueError as e:
            return False
        return True

    def json_toc(self):
        try:
            j = json.loads(self.table_of_contents_cache)
        except ValueError:
            return []
        for item in j:
            if "&amp;" in item["name"]:
                item["name"] = item["name"].replace("&amp;", "&")
            for c in item["children"]:
                if "&amp;" in c["name"]:
                    c["name"] = c["name"].replace("&amp;", "&")
        return j

    def rendered_toc(self):
        if self.is_json_toc():
            template = loader.get_template("parts/researchtoc.html")
            return template.render({"item": self})
        else:
            return mark_safe(markdown(self.table_of_contents_cache))

    def rendered_abstract(self):
        """
        allows keywords to be specified in abstract and replaced by database
        values
        """
        abstract = self.abstract.rendered
        if "$TOC" in abstract:
            abstract = abstract.replace("<p>$TOC</p>", self.rendered_toc())
        return mark_safe(abstract)

    def visible_tags(self):
        return self.tags.filter(display=True)

    def ordered_outputs(self):
        return self.outputs.all().exclude(order=-1).order_by("order")

    def default_top_output(self):
        options = self.outputs.all()
        options = options.exclude(top_order=-1).order_by("top_order")
        if options.exists():
            return options[0].output_url()
        else:
            return "#"

    def ordered_top_outputs(self):
        return self.outputs.all().exclude(top_order=-1).order_by("top_order")

    def author_list(self):
        return [
            authors.person
            for authors in ItemAuthor.objects.filter(research_item=self).order_by(
                "order"
            )
        ]

    def friendly_date(self):
        return self.date.strftime("%B %Y")

    def licence_template_string(self):
        return "licenses/" + self.licence + ".html"

    def absolute_url(self):
        return settings.SITE_BASE_URL + reverse("item", args=[self.slug])

    def __str__(self):
        return self.title + " (" + self.friendly_date() + ")"

    def share_abstract(self):
        """
        reduced version of abstract for sharing
        """
        if self.subtitle:
            text = self.subtitle
        else:
            text = self.abstract.raw

        text = text.replace("$TOC", "")

        if len(text) > 140:
            text = text[: 140 - 4] + "[..]"
        return text

    def similar_items(self, limit=2):
        """
        find similar based on overlapping number of tags
        """
        minimum_score = 1

        tags = list(self.tags.all())
        ids = set([x.id for x in tags])
        all_items = ResearchItem.objects.filter(tags__in=tags, published=True)
        all_items = all_items.exclude(id=self.id).prefetch_related("tags")
        all_items = all_items.distinct()
        all_items = list(all_items)

        for i in all_items:
            our_ids = set([x.id for x in i.tags.all()])
            i.overlap = len(ids.intersection(our_ids))

        all_items.sort(key=lambda x: x.date, reverse=True)
        all_items.sort(key=lambda x: x.overlap, reverse=True)
        all_items = [x for x in all_items if x.overlap >= minimum_score]

        return all_items[:limit]


class ItemAuthor(models.Model):
    class Meta:
        ordering = ["order"]

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    research_item = models.ForeignKey(ResearchItem, on_delete=models.CASCADE)
    order = models.IntegerField(
        verbose_name="Order",
        help_text="Where in the list of authors should this person appear?",
        default=0,
    )

    def __str__(self):
        return (
            self.person.full_name()
            + ' is an author of "'
            + self.research_item.title
            + ('"" in position %d' % self.order)
        )


class ResearchOutput(models.Model):

    title = models.CharField(max_length=200)

    research_item = models.ForeignKey(
        ResearchItem, related_name="outputs", on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to="outputs/",
        blank=True,
        help_text="If the output is a file we should host ourselves, upload it.",
    )

    url = models.URLField(
        blank=True,
        help_text="If the output is hosted elsewhere (like a journal), what is the URL?",
    )

    button_text_value = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional custom text for the button to get this output.",
    )

    download_count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    top_order = models.IntegerField(default=0, help_text="Order for under image link")

    def output_url(self):
        return reverse("download", args=[self.id])

    def increment_download(self):
        query = ResearchOutput.objects.filter(id=self.id)
        query.update(download_count=F("download_count") + 1)

    def button_url(self):
        if self.file:
            return self.file.url
        else:
            return self.url

    def button_text(self):
        if self.button_text_value:
            return self.button_text_value

        if self.file:
            return "Download"

        else:
            return "View Online"

    def __str__(self):
        return self.title


class Site(models.Model):
    """
    Holds site level information
    - should only have one entry
    """

    site_title = models.CharField(max_length=30, default="")
    default_tag = models.ForeignKey(
        Tag, null=True, blank=True, on_delete=models.CASCADE
    )
    twitter = models.CharField(max_length=30, default="")
    description = models.CharField(max_length=255, default="")

    @classmethod
    def get_default(cls):
        try:
            return cls.objects.all()[0]
        except Exception:
            s = Site()
            s.save()
            return s
