"""
Content-page metadata, feeds, navigation, and experiment opt-outs.
"""

import datetime

from django.urls import reverse

import pytest

from pages.models import OptOut
from pages.views import FeedCache

from .fixtures import (
    create_link,
    create_page,
    create_research_item,
    create_site,
    create_tag,
    create_tag_group,
)

pytestmark = pytest.mark.django_db


def test_page_social_metadata_defaults_and_overrides():
    """
    Expected behavior: page social metadata defaults and overrides.
    """
    page = create_page(title="About the work")

    assert page.get_social_title() == "About the work"
    assert page.get_social_desc() == "About the work"

    page.social_title = "Custom title"
    page.social_description = "Custom description"
    assert page.get_social_title() == "Custom title"
    assert page.get_social_desc() == "Custom description"


def test_feed_cache_fetches_once_until_timeout(monkeypatch):
    """
    Expected behavior: feed cache fetches once until timeout.
    """
    parsed = {
        "entries": [
            {"title": f"Post {number}", "link": f"https://example.com/{number}"}
            for number in range(7)
        ]
    }
    calls = []
    monkeypatch.setattr(
        "pages.views.feedparser.parse", lambda url: calls.append(url) or parsed
    )

    first = list(FeedCache.fetch_feed())
    second = list(FeedCache.fetch_feed())

    assert first == second
    assert len(first) == 5
    assert calls == [FeedCache.feed_url]

    FeedCache._time = datetime.datetime.now() - datetime.timedelta(
        seconds=FeedCache.timeout + 1
    )
    list(FeedCache.fetch_feed())
    assert calls == [FeedCache.feed_url, FeedCache.feed_url]


def test_home_page_creates_page_and_orders_featured_content(client, monkeypatch):
    """
    Expected behavior: home page creates page and orders featured content.
    """
    create_site()
    parent = create_tag(label="Our research", slug="research", front_page_order=1)
    group = create_tag_group(name=parent.label)
    featured_tag = create_tag(featured=True, date=datetime.date(2025, 1, 1))
    featured_tag.tag_groups.add(group)
    featured_item = create_research_item(
        featured=True, date=datetime.date(2024, 1, 1), tags=[parent]
    )
    create_research_item(featured=False, tags=[parent])
    create_research_item(featured=True, published=False, tags=[parent])
    monkeypatch.setattr(FeedCache, "fetch_feed", lambda: iter([]))

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert response.context["page"].slug == "home"
    assert response.context["featured_groups"] == [
        (parent, [featured_tag, featured_item])
    ]


def test_page_detail_uses_slug(client, site):
    """
    Expected behavior: page detail uses slug.
    """
    page = create_page(slug="methodology", content="How the work was done")

    response = client.get(reverse("page", args=[page.slug]))

    assert response.status_code == 200
    assert response.context["page"] == page
    assert b"How the work was done" in response.content


def test_opt_out_is_idempotent_for_allowed_experiment(client):
    """
    Expected behavior: opt out is idempotent for allowed experiment.
    """
    url = reverse("page", kwargs={"experiment": "ps1", "user_id": "abc-123"})

    first = client.get(url)
    second = client.get(url)

    assert first.status_code == second.status_code == 200
    assert b"abc-123 opted-out" in first.content
    assert OptOut.objects.filter(experiment="ps1", user_id="abc-123").count() == 1


def test_opt_out_rejects_unknown_experiment_without_writing(client):
    """
    Expected behavior: opt out rejects unknown experiment without writing.
    """
    response = client.get(
        reverse("page", kwargs={"experiment": "unknown", "user_id": "abc"})
    )

    assert response.status_code == 200
    assert b"not a registered experiment" in response.content
    assert OptOut.objects.count() == 0


def test_navigation_context_excludes_hidden_and_home_entries(client, monkeypatch):
    """
    Expected behavior: navigation context excludes hidden and home entries.
    """
    create_site()
    create_page(slug="home", nav_order=0)
    second = create_page(nav_order=2)
    first = create_page(nav_order=1)
    create_page(nav_order=-1)
    first_link = create_link(order=1)
    second_link = create_link(order=2)
    create_link(order=-1)
    first_tag = create_tag(top_bar=1)
    second_tag = create_tag(top_bar=2)
    create_tag(top_bar=-1)
    monkeypatch.setattr(FeedCache, "fetch_feed", lambda: iter([]))

    response = client.get(reverse("home"))

    assert list(response.context["all_pages"]) == [first, second]
    assert list(response.context["top_links"]) == [first_link, second_link]
    assert list(response.context["top_tags"]) == [first_tag, second_tag]
