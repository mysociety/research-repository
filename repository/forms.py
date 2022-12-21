import os
from urllib.request import urlopen, urlretrieve

from bs4 import BeautifulSoup
from django import forms
from django.core.files import File
from django.utils.text import slugify
from django.utils.timezone import now

from repository.models import ResearchItem, ResearchOutput, Tag


class BlogImport(forms.Form):
    """
    on save extract extra properties by fetching url

    """

    url = forms.URLField()
    featured = forms.BooleanField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    def save(self):
        """
        Download html of url and extract meta properties to create new ResearchItem
        """
        url = self.cleaned_data["url"]
        featured = self.cleaned_data["featured"]
        tags = self.cleaned_data["tags"]

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("meta", attrs={"property": "og:title"})["content"]
        description = soup.find("meta", attrs={"property": "og:description"})["content"]
        image_url = soup.find("meta", attrs={"property": "og:image"})["content"]
        author = soup.find("meta", attrs={"itemprop": "author"})["content"]

        # create ResearchItem
        item = ResearchItem(
            slug=slugify(title),
            date=now(),
            title=title,
            abstract=description,
            featured=featured,
            published=True,
        )

        image_file = urlretrieve(image_url)
        file_obj = File(open(image_file[0], "rb"))
        item.hero.save(os.path.basename(image_url), file_obj)

        item.save()
        item.generate_thumbnail = "B"
        item.generate_thumbnail_from_hero()
        item.save()

        item.tags.set(tags)

        ResearchOutput.objects.create(title="Read online", research_item=item, url=url)

        item.add_authors([author])

        item.create_search_items()

        print(f"Created ResearchItem {item}")

        return item.url()
