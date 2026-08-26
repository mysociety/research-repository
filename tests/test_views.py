"""
Public views, filtering, redirects, tracking, and staff-only workflows.
"""

import json
from datetime import date
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

from repository import views

from .fixtures import (
    create_item_author,
    create_person,
    create_research_item,
    create_research_output,
    create_site,
    create_tag,
    create_tag_display_filter,
)

pytestmark = pytest.mark.django_db


def test_embed_json_filters_by_all_tags_and_limit(client):
    """
    Expected behavior: embed JSON filters by all tags and limit.
    """
    create_site()
    first_tag = create_tag(slug="democracy")
    second_tag = create_tag(slug="participation")
    newest = create_research_item(
        title="Newest", date=date(2025, 1, 1), tags=[first_tag, second_tag]
    )
    create_research_item(date=date(2024, 1, 1), tags=[first_tag, second_tag])
    create_research_item(date=date(2026, 1, 1), tags=[first_tag])
    create_research_item(published=False, tags=[first_tag, second_tag])

    response = client.get("/embed/democracy/participation/limit:1/format:json")

    assert response.status_code == 200
    assert [entry["slug"] for entry in response.json()["items"]] == [newest.slug]


def test_embed_featured_combines_items_and_tags_in_date_order(client):
    """
    Expected behavior: embed featured combines items and tags in date order.
    """
    create_site()
    featured_tag = create_tag(featured=True, date=date(2025, 1, 1))
    featured_item = create_research_item(featured=True, date=date(2024, 1, 1))
    create_research_item(featured=False, date=date(2026, 1, 1))

    response = client.get("/embed/featured/format:json")

    assert [entry["slug"] for entry in response.json()["items"]] == [
        featured_tag.slug,
        featured_item.slug,
    ]


def test_embed_related_uses_similarity(client):
    """
    Expected behavior: embed related uses similarity.
    """
    create_site()
    shared = create_tag()
    source = create_research_item(tags=[shared])
    related = create_research_item(tags=[shared])
    create_research_item(tags=[create_tag()])

    response = client.get(f"/embed/related:{source.slug}/format:json")

    assert [entry["slug"] for entry in response.json()["items"]] == [related.slug]


def test_item_list_only_contains_published_items(client):
    """
    Expected behavior: item list only contains published items.
    """
    create_site()
    published = create_research_item(title="Visible research")
    create_research_item(title="Draft research", published=False)

    response = client.get(reverse("items"))

    assert response.status_code == 200
    assert list(response.context["items"]) == [published]
    assert b"Visible research" in response.content
    assert b"Draft research" not in response.content


def test_item_detail_redirects_when_there_is_one_link_output(client):
    """
    Expected behavior: item detail redirects when there is one link output.
    """
    item = create_research_item(published=False)
    create_research_output(
        research_item=item, url="https://example.com/read-the-research"
    )

    response = client.get(reverse("item", args=[item.slug]))

    assert response.status_code == 302
    assert response.url == "https://example.com/read-the-research"


def test_item_detail_renders_json_ld_when_multiple_outputs(client):
    """
    Expected behavior: item detail renders JSON ld when multiple outputs.
    """
    create_site()
    person = create_person(first_name="Ada", last_name="Lovelace")
    item = create_research_item(title="Evidence", subtitle="A review")
    create_item_author(person=person, research_item=item, order=0)
    create_research_output(research_item=item)
    create_research_output(research_item=item)

    response = client.get(reverse("item", args=[item.slug]))
    metadata = json.loads(response.context["json_ld_representation"])

    assert response.status_code == 200
    assert response.context["item"] == item
    assert metadata["headline"] == "Evidence"
    assert metadata["alternativeHeadline"] == "A review"
    assert metadata["author"][0]["name"] == "Ada Lovelace"


def test_people_list_only_includes_opted_in_people(client):
    """
    Expected behavior: people list only includes opted in people.
    """
    create_site()
    listed = create_person(list_in_people=True)
    create_person(list_in_people=False)

    response = client.get(reverse("people"))

    assert response.status_code == 200
    assert list(response.context["people"]) == [listed]


def test_person_detail_exposes_json_ld(client):
    """
    Expected behavior: person detail exposes JSON ld.
    """
    create_site()
    person = create_person(first_name="Grace", last_name="Hopper")

    response = client.get(reverse("person", args=[person.slug]))
    metadata = json.loads(response.context["json_ld_representation"])

    assert response.status_code == 200
    assert metadata["name"] == "Grace Hopper"


def test_tag_view_uses_ordered_default_filter_and_published_intersection():
    """
    Expected behavior: tag view uses ordered default filter and published intersection.
    """
    main = create_tag(slug="research")
    first_filter = create_tag(slug="reports", display_items_in_years=False)
    second_filter = create_tag(slug="blogs")
    create_tag_display_filter(parent=main, tag=second_filter, order=2)
    create_tag_display_filter(parent=main, tag=first_filter, order=1)
    selected = create_research_item(tags=[main, first_filter])
    create_research_item(tags=[main, second_filter])
    create_research_item(tags=[main, first_filter], published=False)

    view = views.TagView()
    view.kwargs = {"slug1": main.slug}
    result = view.get_object()

    assert result.secondary_tag == first_filter
    assert result.filters == [first_filter, second_filter]
    assert result.display_items_in_years is False
    assert result.selected_items == [selected]


def test_tag_view_groups_adjacent_single_item_years_and_reverses_chronology():
    """
    Expected behavior: tag view groups adjacent single item years and reverses chronology.
    """
    main = create_tag(slug="research")
    older = create_research_item(date=date(2022, 1, 1), tags=[main])
    newer = create_research_item(date=date(2023, 1, 1), tags=[main])

    view = views.TagView()
    view.kwargs = {"slug1": main.slug}
    result = view.get_object()

    assert result.selected_items == [newer, older]
    assert [item.grouped_year for item in result.selected_items] == [
        "2022 - 2023",
        "2022 - 2023",
    ]


def test_missing_tag_returns_404(client):
    """
    Expected behavior: missing tag returns 404.
    """
    response = client.get(reverse("tag", args=["does-not-exist"]))
    assert response.status_code == 404


def test_download_redirect_increments_counter(client):
    """
    Expected behavior: download redirect increments counter.
    """
    output = create_research_output(url="https://example.com/report.pdf")

    response = client.get(reverse("download", args=[output.id]))

    assert response.status_code == 302
    assert response.url == output.url
    output.refresh_from_db()
    assert output.download_count == 1


def test_missing_download_has_explanatory_response(client):
    """
    Expected behavior: missing download has explanatory response.
    """
    response = client.get(reverse("download", args=[999999]))

    assert response.status_code == 200
    assert response.content == b"Download does not exist"


def test_special_output_alias_resolves_pdf_and_missing_format(client):
    """
    Expected behavior: special output alias resolves PDF and missing format.
    """
    item = create_research_item()
    pdf = create_research_output(
        research_item=item, title="PDF download", url="https://example.com/file.pdf"
    )

    response = client.get(
        reverse("download_special", kwargs={"item_slug": item.slug, "output_id": "pdf"})
    )
    missing = client.get(
        reverse(
            "download_special",
            kwargs={"item_slug": item.slug, "output_id": "full_text"},
        )
    )

    assert response.status_code == 302
    assert response.url == pdf.url
    assert missing.content == b"Missing full_text format"


def test_blog_import_requires_staff(client):
    """
    Expected behavior: blog import requires staff.
    """
    response = client.get(reverse("import_blog"))

    assert response.status_code == 200
    assert response.content == b"Need to be staff user to use this feature."


def test_staff_blog_import_delegates_valid_form_save(client, monkeypatch):
    """
    Expected behavior: staff blog import delegates valid form save.
    """
    create_site()
    user = get_user_model().objects.create_user("editor", is_staff=True)
    client.force_login(user)
    expected_url = "/publications/imported"
    saved = []
    monkeypatch.setattr(
        "repository.views.BlogImport.save",
        lambda form: saved.append(form) or expected_url,
    )

    response = client.post(
        reverse("import_blog"),
        {"url": "https://example.com/post", "featured": "on"},
    )

    assert response.status_code == 200
    assert response.context["new_url"] == expected_url
    assert len(saved) == 1


def test_sitemap_is_xml_and_excludes_drafts(client):
    """
    Expected behavior: sitemap is XML and excludes drafts.
    """
    create_site()
    visible = create_research_item()
    create_research_item(published=False)

    response = client.get(reverse("sitemap"))

    assert response.status_code == 200
    assert response["Content-Type"] == "text/xml; charset=utf-8"
    assert visible.absolute_url().encode() in response.content


def test_tracking_preview_returns_pixel_without_external_calls(client, monkeypatch):
    """
    Expected behavior: tracking preview returns pixel without external calls.
    """
    send = []
    monkeypatch.setattr(views, "send_event", lambda *args, **kwargs: send.append(args))

    response = client.get(reverse("open_view"), {"campaign": "*|CAMPAIGN_UID|*"})

    assert response.status_code == 200
    assert response["Content-Type"] == "image/gif"
    assert send == []


def test_tracking_uses_campaign_title_and_sends_aggregate_event(client, monkeypatch):
    """
    Expected behavior: tracking uses campaign title and sends aggregate event.
    """
    campaigns = SimpleNamespace(
        get=lambda campaign_id: {
            "settings": {"title": "Auto Weekly Research", "subject_line": ""}
        }
    )
    mailchimp = SimpleNamespace(set_config=lambda config: None, campaigns=campaigns)
    monkeypatch.setattr(views.mailchimp_marketing, "Client", lambda: mailchimp)
    sent = []
    monkeypatch.setattr(views, "send_event", lambda *args: sent.append(args))

    response = client.get(
        reverse("open_view"), {"campaign": "campaign-1", "audience": "policy"}
    )

    assert response.status_code == 200
    assert sent[0][2:] == (
        "email_open",
        {"campaign": "-weekly-research", "audience": "policy"},
    )


def test_send_event_builds_measurement_protocol_request(monkeypatch, settings):
    """
    Expected behavior: send event builds measurement protocol request.
    """
    settings.DEBUG = True
    monkeypatch.setattr(views.random, "randint", lambda start, end: 42)
    requests = []
    monkeypatch.setattr(
        views.requests,
        "post",
        lambda *args, **kwargs: (
            requests.append((args, kwargs)) or SimpleNamespace(status_code=204)
        ),
    )
    params = {"campaign": "weekly"}

    views.send_event("G-TEST", "secret", "email_open", params)

    args, kwargs = requests[0]
    payload = json.loads(kwargs["data"])
    assert args[0] == "https://www.google-analytics.com/mp/collect"
    assert kwargs["params"] == {"measurement_id": "G-TEST", "api_secret": "secret"}
    assert payload["client_id"] == "42.42"
    assert payload["events"][0]["params"]["debug_mode"] == "1"


def test_send_event_raises_for_failed_measurement_request(monkeypatch):
    """
    Expected behavior: send event raises for failed measurement request.
    """
    monkeypatch.setattr(
        views.requests, "post", lambda *args, **kwargs: SimpleNamespace(status_code=400)
    )

    with pytest.raises(Exception, match="returned status code 400"):
        views.send_event("G-TEST", "secret", "email_open", {})
