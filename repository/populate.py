"""
Creates tests data for testing framework
"""
from .models import (
    Tag,
    Person,
    ResearchItem,
    ItemAuthor,
    ResearchOutput,
    Site,
    TagDisplayFilter,
    ResearchLicence,
)
from pages.models import Page
from django.contrib.auth.models import User
from datetime import datetime
import random


def prepare_people():
    print("preparing people")
    gc = Person.objects.get_or_create

    gc(
        first_name="Test",
        last_name="User",
        institution="Test Charity",
        slug="test_user_1",
    )

    gc(
        first_name="Test",
        last_name="User With URL",
        institution="Test Charity",
        url="https://www.mysociety.org/",
        link_behaviour="url",
        slug="test_user_2",
    )


def prepare_tags():
    print("preparing tags")
    gc = Tag.objects.get_or_create
    tgc = TagDisplayFilter.objects.get_or_create

    r, c = gc(
        label="Our Research",
        slug="research",
        description="Test Site Research",
        top_bar=1,
        front_page_order=True,
    )

    t, c = gc(
        label="Papers/Reports", slug="papers", description="Test Papers and Reports"
    )

    tgc(parent=r, tag=t)  # create TagDisplayFilter examples

    t, c = gc(label="Blog Posts", slug="blog_posts", description="Test Blog Posts")

    tgc(parent=r, tag=t)

    t, c = gc(
        label="Exploration Sites", slug="minisites", description="Test Mini Sites"
    )

    tgc(parent=r, tag=t)

    gc(
        label="Hidden Category",
        slug="hidden",
        description="Does not appear on menus",
        display=False,
    )

    gc(
        label="Display In Years",
        slug="years",
        description="Shows research in years",
        display_items_in_years=True,
    )

    gc(
        label="Display Without Years",
        slug="no_years",
        description="Shows research without year listings",
        display_items_in_years=False,
    )

    gc(label="Policy", slug="policy", description="Test Policy", top_bar=2)


def prepare_site():
    "preparing site information"
    s = Site.get_default()
    s.site_title = "Test Research Repo"
    s.default_tag = Tag.objects.get(slug="research")
    s.twitter = "mysociety"
    s.description = "Test research repositiory."
    s.save()


def random_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)


def prepare_pages():
    gc = Page.objects.get_or_create

    gc(
        title="Test Page",
        slug="test_page",
        content="This is a test of a basic page",
        nav_order=1,
    )


def prepare_research_items():
    print("preparing research items")
    ResearchItem.objects.all().delete()

    master_tags = list(Tag.objects.filter(slug__in=["research", "policy"]))
    tags = list(Tag.objects.all().exclude(slug__in=["research", "policy"]))
    authors = list(Person.objects.all())

    all_items = []
    for x in range(1, 21):

        letter = chr(x + 64)

        r = ResearchItem(
            title="Item {0}".format(letter),
            date=random_date(2015, 2018),
            slug="item_{0}".format(letter),
            published=True,
            licence="cc-by-3.0",
        )
        r.save()

        # add random authors
        author_range = random.randint(1, len(authors))
        if author_range == len(authors):
            authors = [x for x in authors]
        else:
            authors = [random.choice(authors) for x in range(0, author_range)]

        for x, a in enumerate(authors):
            ItemAuthor(person=a, research_item=r, order=x + 1).save()

        # add random tags
        # either policy or research
        tags_to_add = []
        tags_to_add.append(random.choice(master_tags))

        # then random other ones
        tag_range = random.randint(0, 3)
        tags_to_add.extend([random.choice(tags) for x in range(0, tag_range)])
        for x, a in enumerate(tags_to_add):
            r.tags.add(a)

        # add a few outputs
        gc = ResearchOutput.objects.get_or_create
        gc(
            title="Download Now!",
            url="http://mysociety.org",
            order=0,
            top_order=0,
            research_item=r,
        )
        gc(
            title="View Online!",
            url="http://mysociety.org",
            order=0,
            top_order=0,
            research_item=r,
        )

        author_text = ", ".join([x.full_name() for x in authors])
        tag_text = ", ".join([x.label for x in tags_to_add])
        abstract = "This is a test item, written by {0}. It has the following tags: {1}"
        r.abstract = abstract.format(author_text, tag_text)
        r.save()

        all_items.append(r)

    # elevate a few to featured
    for x in range(0, 4):
        r = random.choice(all_items)
        r.featured = True
        r.save()


def create_licences():
    print("preparing research licence")
    gc = ResearchLicence.objects.get_or_create

    gc(
        slug="cc-by-4.0",
        name="Attribution 4.0 International (CC BY 4.0)",
        url="https://creativecommons.org/licenses/by/4.0/",
    )


def create_super_user():
    print("creating superuser")
    if User.objects.filter(username="admin").exists() == False:
        User.objects.create_superuser("admin", "admin-test@mysociety.org", "admin")


def populate():
    create_super_user()
    prepare_tags()
    prepare_people()
    prepare_site()
    prepare_pages()
    prepare_research_items()
    create_licences()
