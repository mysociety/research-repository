"""
Domain-model validation, relationships, ordering, and serialization.
"""

import json
from datetime import date

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import pytest

from repository.models import Person, ResearchLicence, SearchItem, Site

from .fixtures import (
    build_tag,
    create_item_author,
    create_mini_site,
    create_person,
    create_research_item,
    create_research_output,
    create_tag,
    create_tags,
)

pytestmark = pytest.mark.django_db


def test_tag_name_url_and_social_description(settings):
    """
    Expected behavior: tag name URL and social description.
    """
    tag = create_tag(label="", slug="open-data", description="x" * 251)

    assert tag.nice_name() == "Open Data"
    assert tag.title == ""
    assert tag.url() == reverse("tag", args=["open-data"])
    assert tag.absolute_url() == settings.SITE_BASE_URL + tag.url()
    assert tag.get_social_description() == "x" * 250 + "[...]"


def test_tag_requires_hero_when_generating_thumbnail():
    """
    Expected behavior: tag requires hero when generating thumbnail.
    """
    tag = build_tag(generate_thumbnail="R", hero=None)

    with pytest.raises(ValidationError, match="no hero uploaded"):
        tag.clean()


def test_tag_research_items_are_published_and_reverse_chronological():
    """
    Expected behavior: tag research items are published and reverse chronological.
    """
    tag = create_tag()
    older = create_research_item(date=date(2022, 1, 1), tags=[tag])
    newer = create_research_item(date=date(2024, 1, 1), tags=[tag])
    create_research_item(date=date(2025, 1, 1), published=False, tags=[tag])

    assert list(tag.get_research_items()) == [newer, older]
    assert tag.count() == 2


def test_person_from_name_handles_compound_first_name_and_reuses_record():
    """
    Expected behavior: person from name handles compound first name and reuses record.
    """
    first = Person.get_person_from_name("Mary Jane Watson")
    second = Person.get_person_from_name("Mary Jane Watson")

    assert first == second
    assert (first.first_name, first.last_name, first.slug) == (
        "Mary Jane",
        "Watson",
        "mary-jane-watson",
    )


def test_person_preferred_urls_and_json_ld(settings):
    """
    Expected behavior: person preferred urls and JSON ld.
    """
    person = create_person(
        first_name="Ada",
        last_name="Lovelace",
        institution="Analytical Society",
        link_behaviour="url",
        url="https://example.com/ada",
        orcid="0000-0000-0000-0001",
        twitter="ada",
    )

    data = person.json_ld_representation()

    assert person.preferred_url() == person.url
    assert data["name"] == "Ada Lovelace"
    assert data["affiliation"]["name"] == "Analytical Society"
    assert person.url in data["sameAs"]
    assert "http://orcid.org/0000-0000-0000-0001" in data["sameAs"]
    assert (
        settings.SITE_BASE_URL + reverse("person", args=[person.slug]) in data["sameAs"]
    )


def test_person_items_list_uses_item_date_order():
    """
    Expected behavior: person items list uses item date order.
    """
    person = create_person()
    older = create_research_item(date=date(2020, 1, 1))
    newer = create_research_item(date=date(2023, 1, 1))
    create_item_author(person=person, research_item=older)
    create_item_author(person=person, research_item=newer)

    assert person.items_list() == [newer, older]


def test_research_item_add_authors_preserves_order_and_does_not_overwrite():
    """
    Expected behavior: research item add authors preserves order and does not overwrite.
    """
    item = create_research_item()
    item.add_authors(["Ada Lovelace", "Grace Hopper"])

    assert [person.full_name() for person in item.author_list()] == [
        "Ada Lovelace",
        "Grace Hopper",
    ]

    item.add_authors(["Katherine Johnson"])
    assert [person.full_name() for person in item.author_list()] == [
        "Ada Lovelace",
        "Grace Hopper",
    ]


def test_research_item_migrates_legacy_licence():
    """
    Expected behavior: research item migrates legacy licence.
    """
    item = create_research_item(licence="cc-by-3.0", licencing=None)

    item.migrate_licence()

    item.refresh_from_db()
    assert item.licencing.slug == "cc-by-3.0"
    assert ResearchLicence.objects.filter(slug="cc-by-3.0").count() == 1


def test_research_item_identifies_special_outputs():
    """
    Expected behavior: research item identifies special outputs.
    """
    item = create_research_item()
    pdf = create_research_output(research_item=item, title="Download PDF")
    online = create_research_output(research_item=item, title="Read online")

    assert item.special_urls() == {"pdf": pdf, "full_text": online}


def test_research_item_toc_supports_json_and_markdown():
    """
    Expected behavior: research item TOC supports JSON and markdown.
    """
    item = create_research_item(
        table_of_contents_cache=json.dumps(
            [{"name": "A &amp; B", "children": [{"name": "C &amp; D"}]}]
        )
    )

    assert item.is_json_toc() is True
    assert item.json_toc()[0] == {
        "name": "A & B",
        "children": [{"name": "C & D"}],
    }

    item.table_of_contents_cache = "## Contents"
    assert item.is_json_toc() is False
    assert item.json_toc() == []
    assert "<h2>Contents</h2>" in item.rendered_toc()


def test_research_item_abstract_can_embed_toc(monkeypatch):
    """
    Expected behavior: research item abstract can embed TOC.
    """
    item = create_research_item(abstract="Before\n\n$TOC\n\nAfter")
    monkeypatch.setattr(item, "rendered_toc", lambda: "<nav>toc</nav>")

    rendered = item.rendered_abstract()

    assert "<nav>toc</nav>" in rendered
    assert "$TOC" not in rendered


def test_research_item_orders_and_filters_tags_and_outputs():
    """
    Expected behavior: research item orders and filters tags and outputs.
    """
    item = create_research_item()
    visible = create_tag(display=True, is_project=True)
    hidden = create_tag(display=False)
    item.tags.set([visible, hidden])
    last = create_research_output(research_item=item, order=2, top_order=3)
    first = create_research_output(research_item=item, order=1, top_order=1)
    create_research_output(research_item=item, order=-1, top_order=-1)

    assert list(item.visible_tags()) == [visible]
    assert list(item.projects()) == [visible]
    assert list(item.ordered_outputs()) == [first, last]
    assert list(item.ordered_top_outputs()) == [first, last]
    assert item.default_top_output() == first.output_url()


def test_research_item_similar_items_prefers_overlap_then_date():
    """
    Expected behavior: research item similar items prefers overlap then date.
    """
    primary, secondary = create_tags(2)
    item = create_research_item(tags=[primary, secondary])
    high_overlap = create_research_item(
        date=date(2020, 1, 1), tags=[primary, secondary]
    )
    recent_one_tag = create_research_item(date=date(2025, 1, 1), tags=[primary])
    create_research_item(published=False, tags=[primary, secondary])
    create_research_item(tags=[create_tag()])

    assert item.similar_items() == [high_overlap, recent_one_tag]


@pytest.mark.parametrize(
    ("title", "has_file", "expected"),
    [
        ("Supporting data", True, True),
        ("Download the report", False, True),
        ("Read online", False, False),
    ],
)
def test_research_output_downloadable(title, has_file, expected):
    """
    Expected behavior: research output downloadable.
    """
    uploaded = SimpleUploadedFile("data.csv", b"value") if has_file else None
    output = create_research_output(title=title, file=uploaded)

    assert output.downloadable() is expected


def test_research_output_button_and_atomic_download_count():
    """
    Expected behavior: research output button and atomic download count.
    """
    output = create_research_output(
        url="https://example.com/report", button_text_value="Read report"
    )

    output.increment_download()
    output.refresh_from_db()

    assert output.download_count == 1
    assert output.button_url() == "https://example.com/report"
    assert output.button_text() == "Read report"


def test_site_get_default_creates_once():
    """
    Expected behavior: site get default creates once.
    """
    assert Site.objects.count() == 0

    first = Site.get_default()
    second = Site.get_default()

    assert first == second
    assert Site.objects.count() == 1


def test_search_item_bulk_create_sends_post_save(monkeypatch):
    """
    Expected behavior: search item bulk create sends post save.
    """
    item = create_research_item()
    pending = SearchItem(
        research_item=item, title="Section", url="/section", text="Text"
    )
    sent = []

    from django.db.models.signals import post_save

    monkeypatch.setattr(post_save, "send", lambda *args, **kwargs: sent.append(kwargs))
    SearchItem.bulk_create_with_signal([pending])

    assert SearchItem.objects.count() == 1
    assert sent[0]["created"] is True


def test_minisite_url_uses_site_configuration(settings):
    """
    Expected behavior: minisite URL uses site configuration.
    """
    site = create_mini_site(site_folder="budget-tool")

    assert site.url() == settings.SITE_BASE_URL + settings.SITES_URL + "budget-tool/"
