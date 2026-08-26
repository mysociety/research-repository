"""Small, explicit test-object builders.

Each ``create_*`` helper saves a model with valid, deterministic defaults. Keyword
arguments override those defaults so individual tests only state values relevant to
the behavior under test. Helpers also create required related objects when omitted.
"""

from datetime import date
from itertools import count

from pages.models import Link, MiniSite, OptOut, Page
from repository.models import (
    ItemAuthor,
    Person,
    ResearchItem,
    ResearchLicence,
    ResearchOutput,
    Site,
    Tag,
    TagDisplayFilter,
    TagGroup,
)

_sequences = {}


def _next(name):
    """Return a value unique to this model type within the current test."""
    return next(_sequences.setdefault(name, count()))


def reset_fixture_sequences():
    """Reset generated values so tests remain deterministic in any run order."""
    _sequences.clear()


def create_page(**overrides):
    """Create a content page; content follows an overridden title by default."""
    number = _next("page")
    title = overrides.pop("title", f"Page {number}")
    values = {
        "title": title,
        "slug": f"page-{number}",
        "content": f"Content for {title}",
        **overrides,
    }
    return Page.objects.create(**values)


def create_link(**overrides):
    """Create a navigation link with a unique external URL."""
    number = _next("link")
    values = {
        "label": f"Link {number}",
        "url": f"https://example.com/{number}",
        "order": 0,
        **overrides,
    }
    return Link.objects.create(**values)


def create_opt_out(**overrides):
    """Create an opt-out record for the supported test experiment."""
    values = {
        "experiment": "ps1",
        "user_id": f"user-{_next('opt_out')}",
        **overrides,
    }
    return OptOut.objects.create(**values)


def create_mini_site(**overrides):
    """Create a mini-site whose name and folder default to its slug."""
    slug = overrides.pop("slug", f"site-{_next('mini_site')}")
    values = {
        "slug": slug,
        "name": slug.title(),
        "site_folder": slug,
        **overrides,
    }
    return MiniSite.objects.create(**values)


def create_research_licence(**overrides):
    """Create a licence whose display name defaults to its slug."""
    slug = overrides.pop("slug", f"licence-{_next('research_licence')}")
    values = {"slug": slug, "name": slug.title(), **overrides}
    return ResearchLicence.objects.create(**values)


def create_tag_group(**overrides):
    """Create a tag group with a non-empty description."""
    values = {
        "name": f"Group {_next('tag_group')}",
        "description": "A group of related tags",
        **overrides,
    }
    return TagGroup.objects.create(**values)


def tag_values(**overrides):
    """Return shared valid values for saved and unsaved tags."""
    number = _next("tag")
    return {
        "label": f"Tag {number}",
        "slug": f"tag-{number}",
        "date": date(2024, 1, 1),
        "description": "A research category",
        **overrides,
    }


def build_tag(**overrides):
    """Build, but do not save, a tag for model validation tests."""
    return Tag(**tag_values(**overrides))


def create_tag(**overrides):
    """Create a tag with a stable date and unique label and slug."""
    return Tag.objects.create(**tag_values(**overrides))


def create_tags(quantity, **overrides):
    """Create several tags sharing the supplied overrides."""
    return [create_tag(**overrides) for _ in range(quantity)]


def create_tag_display_filter(**overrides):
    """Create a display filter, creating its parent and tag when omitted."""
    values = {
        "parent": overrides.pop("parent", None) or create_tag(),
        "tag": overrides.pop("tag", None) or create_tag(),
        "order": 0,
        **overrides,
    }
    return TagDisplayFilter.objects.create(**values)


def create_person(**overrides):
    """Create a person with a slug derived from their effective name."""
    number = _next("person")
    first_name = overrides.pop("first_name", f"First{number}")
    last_name = overrides.pop("last_name", f"Last{number}")
    values = {
        "first_name": first_name,
        "last_name": last_name,
        "slug": f"{first_name}-{last_name}".lower(),
        **overrides,
    }
    return Person.objects.create(**values)


def create_research_item(**overrides):
    """Create an item and attach optional tags and ordered people relations."""
    number = _next("research_item")
    tags = overrides.pop("tags", ())
    people = overrides.pop("people", ())
    values = {
        "title": f"Research item {number}",
        "slug": f"research-item-{number}",
        "date": date(2024, 1, 1),
        "published": True,
        "abstract": "A useful research abstract",
        **overrides,
    }
    item = ResearchItem.objects.create(**values)
    if tags:
        item.tags.set(tags)
    for order, person in enumerate(people):
        ItemAuthor.objects.create(research_item=item, person=person, order=order)
    return item


def create_item_author(**overrides):
    """Create an authorship, including missing person or item records."""
    values = {
        "person": overrides.pop("person", None) or create_person(),
        "research_item": overrides.pop("research_item", None) or create_research_item(),
        "order": overrides.pop("order", _next("item_author")),
        **overrides,
    }
    return ItemAuthor.objects.create(**values)


def create_research_output(**overrides):
    """Create an output, including a research item when one is omitted."""
    number = _next("research_output")
    values = {
        "title": f"Output {number}",
        "research_item": overrides.pop("research_item", None) or create_research_item(),
        "url": f"https://example.com/output/{number}",
        **overrides,
    }
    return ResearchOutput.objects.create(**values)


def create_site(**overrides):
    """Create site configuration, including a default tag when omitted."""
    values = {
        "site_title": "Research Repository",
        "default_tag": overrides.pop("default_tag", None) or create_tag(),
        "twitter": "research",
        "description": "Research and evidence",
        **overrides,
    }
    return Site.objects.create(**values)
