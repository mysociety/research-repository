"""
Rare branches, fallbacks, integrations, and administrative hooks.
"""

import io
import json
from datetime import date
from pathlib import Path
from types import SimpleNamespace

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse

import pytest
from mailchimp_marketing.api_client import ApiClientError
from PIL import Image, ImageFont

from pages import admin as pages_admin
from pages.models import (
    MiniSite,
)
from pages.models import (
    OverwriteStorage as PageOverwriteStorage,
)
from repository import admin as repository_admin
from repository import views
from repository.image_processor import ThumbNailCreator
from repository.models import (
    OverwriteStorage,
    ResearchItem,
    SearchItem,
)

from .fixtures import (
    create_item_author,
    create_link,
    create_mini_site,
    create_opt_out,
    create_page,
    create_person,
    create_research_item,
    create_research_licence,
    create_research_output,
    create_site,
    create_tag,
    create_tag_group,
)
from .test_api_and_files import zip_bytes

pytestmark = pytest.mark.django_db


def test_storage_overwrite_classes_delete_existing_name(monkeypatch):
    """
    Expected behavior: storage overwrite classes delete existing name.
    """
    for storage_class in (OverwriteStorage, PageOverwriteStorage):
        storage = storage_class()
        deleted = []
        monkeypatch.setattr(storage, "delete", deleted.append)

        assert storage.get_available_name("same.zip", max_length=3) == "same.zip"
        assert deleted == ["same.zip"]


def test_model_strings_and_simple_fallbacks():
    """
    Expected behavior: model strings and simple fallbacks.
    """
    licence = create_research_licence(slug="cc-by-4.0")
    group = create_tag_group(name="Methods")
    tag = create_tag(label="", slug="evidence", date=None)
    person = create_person(first_name="Ada", last_name="Lovelace")
    item = create_research_item(
        title="Report", date=date(2024, 2, 1), licence="cc-by-3.0"
    )
    authorship = create_item_author(person=person, research_item=item, order=2)
    output = create_research_output(title="Website", research_item=item)
    search = SearchItem.objects.create(
        research_item=item, title="Chapter", url="/chapter", text="A long chapter body"
    )
    page = create_page(title="About")
    link = create_link(label="External")
    optout = create_opt_out(user_id="reader-1")

    assert str(licence) == "cc-by-4.0"
    assert str(group) == "Methods"
    assert str(tag) == "Evidence"
    assert tag.friendly_date() == ""
    assert str(person) == "Ada Lovelace"
    assert str(item) == "Report (February 2024)"
    assert item.licence_template_string() == "licenses/cc-by-3.0.html"
    assert "Ada Lovelace" in str(authorship)
    assert str(output) == "Website"
    assert str(search) == "Chapter - A long chapter body"
    assert str(page) == "About"
    assert str(link) == "External"
    assert str(optout) == "reader-1"


def test_tag_json_images_social_override_and_plain_slug(settings):
    """
    Expected behavior: tag JSON images social override and plain slug.
    """
    tag = create_tag(
        label="",
        slug="evidence",
        social_description="Share this category",
        hero=SimpleUploadedFile("hero.png", b"hero"),
        thumbnail=SimpleUploadedFile("thumb.png", b"thumb"),
    )

    data = tag.json()

    assert tag.nice_name() == "Evidence"
    assert tag.get_social_description() == "Share this category"
    assert data["hero_image"].startswith(settings.SITE_BASE_URL)
    assert data["thumbnail"].startswith(settings.SITE_BASE_URL)
    assert data["authors"] == []


def test_person_profile_and_all_alternate_identifiers():
    """
    Expected behavior: person profile and all alternate identifiers.
    """
    person = create_person(
        link_behaviour="profile-page",
        url="https://example.com/profile",
        googlescholar="scholar-id",
        researcherid="researcher-id",
    )

    data = person.json_ld_representation()

    assert person.preferred_url() == person.absolute_url()
    assert "https://scholar.google.co.uk/citations?user=scholar-id" in data["sameAs"]
    assert "http://www.researcherid.com/rid/researcher-id" in data["sameAs"]


def test_thumbnail_mixin_skip_generate_and_save_generated_file(monkeypatch, tmp_path):
    """
    Expected behavior: thumbnail mixin skip generate and save generated file.
    """
    hero_path = tmp_path / "hero.png"
    hero_path.write_bytes(b"source")
    item = create_research_item(hero=SimpleUploadedFile("hero.png", b"source"))

    item.generate_thumbnail = ""
    assert item.generate_thumbnail_from_hero() is None

    item.generate_thumbnail = "R"
    monkeypatch.setattr(
        ThumbNailCreator,
        "convert_hero_image_to_thumbnail",
        lambda self, source, text: io.BytesIO(b"generated-png"),
    )
    item.generate_thumbnail_from_hero()

    item.refresh_from_db()
    assert item.thumbnail.name.endswith(f"{item.slug}-thumbnail.png")
    assert item.thumbnail.read() == b"generated-png"


def test_research_item_json_social_thumbnail_and_empty_defaults(settings):
    """
    Expected behavior: research item JSON social thumbnail and empty defaults.
    """
    person = create_person(first_name="Grace", last_name="Hopper")
    item = create_research_item(
        social_description="Custom share copy",
        hero=SimpleUploadedFile("hero.png", b"hero"),
        thumbnail=SimpleUploadedFile("thumb.png", b"thumb"),
        people=[person],
    )

    data = item.json()

    assert item.has_thumbnail() is True
    assert item.get_social_description() == "Custom share copy"
    assert data["thumbnail"].startswith(settings.SITE_BASE_URL)
    assert data["hero_image"].startswith(settings.SITE_BASE_URL)
    assert data["authors"][0]["name"] == "Grace Hopper"

    empty = create_research_item(abstract="x" * 251)
    assert empty.has_thumbnail() is False
    assert empty.get_social_description() == "x" * 250 + "[...]"
    assert empty.default_top_output() == "#"


def test_research_item_share_abstract_and_render_without_toc():
    """
    Expected behavior: research item share abstract and render without TOC.
    """
    item = create_research_item(subtitle="", abstract="Body $TOC " + "x" * 160)

    assert item.share_abstract().endswith("[..]")
    assert "$TOC" not in item.share_abstract()
    assert "Body" in item.rendered_abstract()

    item.subtitle = "Short subtitle"
    assert item.share_abstract() == "Short subtitle"


def test_research_output_file_and_default_buttons():
    """
    Expected behavior: research output file and default buttons.
    """
    file_output = create_research_output(
        title="Data",
        file=SimpleUploadedFile("data.csv", b"value"),
        button_text_value="",
    )
    online_output = create_research_output(title="Web page", button_text_value="")

    assert file_output.button_url().endswith("data.csv")
    assert file_output.button_text() == "Download"
    assert online_output.button_text() == "View Online"


@pytest.mark.parametrize("title", ["EPUB edition", "Kindle version", "PDF version"])
def test_research_output_recognizes_download_titles(title):
    """
    Expected behavior: research output recognizes download titles.
    """
    assert create_research_output(title=title, file=None).downloadable() is True


def test_toc_fetch_failure_json_render_and_unescaped_names(monkeypatch):
    """
    Expected behavior: TOC fetch failure JSON render and unescaped names.
    """
    item = create_research_item(
        table_of_contents_url="https://example.com/toc.json",
        table_of_contents_cache=json.dumps(
            [{"name": "Intro", "children": [{"name": "Child"}]}]
        ),
    )
    monkeypatch.setattr(
        "repository.models.urllib.request.urlopen",
        lambda url: (_ for _ in ()).throw(OSError("offline")),
    )

    item.fetch_toc(save=True)

    assert item.json_toc() == [{"name": "Intro", "children": [{"name": "Child"}]}]
    assert "<ol>" in item.rendered_toc()

    no_url = create_research_item(table_of_contents_url="")
    no_url.fetch_toc()
    assert no_url.table_of_contents_cache == ""


def test_complete_stringprint_archive_hydrates_blank_item_and_all_outputs(
    settings, monkeypatch
):
    """
    Expected behavior: complete stringprint archive hydrates blank item and all outputs.
    """
    metadata = {
        "title": "Imported title",
        "subtitle": "Imported subtitle",
        "publish_date": "2023-05-06",
        "description": "Imported abstract",
        "authors": "Ada Lovelace,Grace Hopper",
        "header": {"credit": "Photo by Researcher"},
    }
    archive = zip_bytes(
        {
            "index.html": "<h1>Report</h1>",
            "plain.html": "Plain report",
            "toc.json": "[]",
            "complete.mobi": b"mobi",
            "complete.epub": b"epub",
            "complete.pdf": b"pdf",
            "settings-for-render.json": json.dumps(metadata),
        }
    )
    item = create_research_item(title="Temporary", slug="complete")
    item.zip_archive.save("complete.zip", SimpleUploadedFile("complete.zip", archive))
    item.title = ""
    item.subtitle = ""
    item.date = None
    item.abstract = ""
    item.photo_credit = ""
    item.licencing = None
    fetched = []
    searched = []
    monkeypatch.setattr(item, "fetch_toc", lambda save: fetched.append(save))
    monkeypatch.setattr(item, "create_search_items", lambda: searched.append(item.pk))

    item.unpack_archive()

    item.refresh_from_db()
    assert (item.title, item.subtitle) == ("Imported title", "Imported subtitle")
    assert item.date == date(2023, 5, 6)
    assert item.abstract.raw == "Imported abstract"
    assert item.photo_credit.raw == "Photo by Researcher"
    assert item.licencing.slug == "cc-by-4.0"
    assert fetched == [True]
    assert searched == [item.pk]
    assert set(item.outputs.values_list("title", flat=True)) == {
        "Read Online",
        "Plain Text",
        "Kindle .mobi",
        "epub",
        "PDF",
    }
    assert [author.full_name() for author in item.author_list()] == [
        "Ada Lovelace",
        "Grace Hopper",
    ]

    old_file = Path(settings.ZIP_ROOT) / "complete" / "old.txt"
    old_file.write_text("remove me")
    item.unpack_archive()
    assert not old_file.exists()
    assert item.outputs.count() == 5


def test_unpack_archive_without_file_returns_none():
    """
    Expected behavior: unpack archive without file returns None.
    """
    assert create_research_item(zip_archive=None).unpack_archive() is None
    assert create_mini_site(zip_archive=None).unpack_archive() is None


def test_thumbnail_creator_all_labels_destination_and_folder(monkeypatch, tmp_path):
    """
    Expected behavior: thumbnail creator all labels destination and folder.
    """
    source = tmp_path / "hero.png"
    Image.new("RGB", (220, 220), color=(20, 80, 160)).save(source)
    monkeypatch.setattr(
        "repository.image_processor.ColorThief",
        lambda path: SimpleNamespace(
            get_palette=lambda color_count: [(20, 80, 160), (200, 10, 10)]
        ),
    )
    default_font = ImageFont.load_default()
    monkeypatch.setattr(
        "repository.image_processor.ImageFont.truetype",
        lambda path, size: default_font,
    )

    for label in ["R", "P", "C", "M", "S"]:
        destination = tmp_path / f"{label}.png"
        assert (
            ThumbNailCreator.convert_hero_image_to_thumbnail(
                source, dest=destination, text=label
            )
            is None
        )
        assert Image.open(destination).size == (110, 150)

    source_folder = tmp_path / "sources"
    destination_folder = tmp_path / "destinations"
    source_folder.mkdir()
    destination_folder.mkdir()
    Image.new("RGB", (220, 220), color=(20, 80, 160)).save(source_folder / "one.png")
    calls = []
    monkeypatch.setattr(
        ThumbNailCreator,
        "convert_hero_image_to_thumbnail",
        lambda origin, dest: calls.append((origin, dest)),
    )
    ThumbNailCreator.convert_folder(source_folder, destination_folder)
    assert calls == [
        (str(source_folder / "one.png"), str(destination_folder / "one.png"))
    ]


def test_admin_actions_delegate_to_every_selected_object():
    """
    Expected behavior: admin actions delegate to every selected object.
    """
    objects = [SimpleNamespace(migrate_licence=lambda: None) for _ in range(2)]
    searches = [SimpleNamespace(create_search_items=lambda: None) for _ in range(3)]
    migrated = []
    indexed = []
    for number, obj in enumerate(objects):
        obj.migrate_licence = lambda number=number: migrated.append(number)
    for number, obj in enumerate(searches):
        obj.create_search_items = lambda number=number: indexed.append(number)

    repository_admin.migrate_licence(None, None, objects)
    repository_admin.create_search_items(None, None, searches)

    assert migrated == [0, 1]
    assert indexed == [0, 1, 2]


def test_research_and_tag_admin_save_hooks(monkeypatch):
    """
    Expected behavior: research and tag admin save hooks.
    """
    request = RequestFactory().post("/admin/")
    item = create_research_item(generate_thumbnail="R", thumbnail=None)
    item_calls = []
    monkeypatch.setattr(
        item, "fetch_toc", lambda save: item_calls.append(("toc", save))
    )
    monkeypatch.setattr(
        item, "generate_thumbnail_from_hero", lambda: item_calls.append(("thumbnail",))
    )
    monkeypatch.setattr(item, "unpack_archive", lambda: item_calls.append(("unpack",)))
    monkeypatch.setattr(
        item, "create_search_items", lambda: item_calls.append(("search",))
    )
    form = SimpleNamespace(changed_data=["zip_archive"])

    repository_admin.ResearchItemAdmin(ResearchItem, admin.site).save_model(
        request, item, form, False
    )

    assert item_calls == [
        ("toc", False),
        ("thumbnail",),
        ("unpack",),
        ("search",),
    ]

    tag = create_tag(generate_thumbnail="R", thumbnail=None)
    tag_calls = []
    monkeypatch.setattr(
        tag, "generate_thumbnail_from_hero", lambda: tag_calls.append(True)
    )
    repository_admin.TagItemAdmin(type(tag), admin.site).save_model(
        request, tag, SimpleNamespace(changed_data=[]), False
    )
    assert tag_calls == [True]


def test_minisite_admin_unpack_hook(monkeypatch):
    """
    Expected behavior: minisite admin unpack hook.
    """
    request = RequestFactory().post("/admin/")
    site = create_mini_site()
    calls = []
    monkeypatch.setattr(site, "unpack_archive", lambda: calls.append(True))

    pages_admin.MiniSiteAdmin(MiniSite, admin.site).save_model(
        request, site, SimpleNamespace(changed_data=["zip_archive"]), False
    )

    assert calls == [True]


def test_snippet_related_template_and_text_options(client, monkeypatch):
    """
    Expected behavior: snippet related template and text options.
    """
    base = create_research_item()
    related = create_research_item()
    monkeypatch.setattr(ResearchItem, "similar_items", lambda item, limit: [related])

    response = client.get(
        reverse(
            "embed",
            args=[f"related:{base.slug}/limit:1/template:standard/text:false"],
        )
    )

    assert response.status_code == 200
    assert list(response.context["items"]) == [related]
    assert response.context["related"] is True
    assert response.context["display_text"] is False


def test_item_json_ld_uses_uploaded_thumbnail(client):
    """
    Expected behavior: item JSON ld uses uploaded thumbnail.
    """
    create_site()
    item = create_research_item(thumbnail=SimpleUploadedFile("thumb.png", b"thumb"))
    create_research_output(research_item=item)
    create_research_output(research_item=item)

    response = client.get(reverse("item", args=[item.slug]))
    metadata = json.loads(response.context["json_ld_representation"])

    assert metadata["image"].endswith(item.thumbnail.url)


def test_tag_context_and_explicit_secondary_filter(client):
    """
    Expected behavior: tag context and explicit secondary filter.
    """
    create_site()
    main = create_tag(top_bar=0)
    other_top = create_tag(top_bar=1)
    secondary = create_tag()
    selected = create_research_item(tags=[main, secondary])

    response = client.get(reverse("tag", args=[main.slug, secondary.slug]))

    assert response.status_code == 200
    assert response.context["top_tags"] == [main, other_top]
    assert response.context["tag"].secondary_tag == secondary
    assert response.context["tag"].filters == [secondary]
    assert response.context["tag"].selected_items == [selected]


def test_non_top_tag_context_hides_top_navigation(client):
    """
    Expected behavior: non top tag context hides top navigation.
    """
    create_site()
    create_tag(top_bar=0)
    plain = create_tag(top_bar=-1)

    response = client.get(reverse("tag", args=[plain.slug]))

    assert response.status_code == 200
    assert response.context["top_tags"] == []


def test_staff_blog_import_get_and_invalid_post(client):
    """
    Expected behavior: staff blog import get and invalid post.
    """
    create_site()
    user = get_user_model().objects.create_user("staff", is_staff=True)
    client.force_login(user)

    get_response = client.get(reverse("import_blog"))
    post_response = client.post(reverse("import_blog"), {"url": "not-a-url"})

    assert get_response.status_code == post_response.status_code == 200
    assert get_response.context["new_url"] is None
    assert post_response.context["form"].errors


def test_special_download_delegates_non_alias_id(client):
    """
    Expected behavior: special download delegates non alias id.
    """
    output = create_research_output(url="https://example.com/data.csv")

    response = client.get(
        reverse(
            "download_special",
            kwargs={"item_slug": output.research_item.slug, "output_id": output.id},
        )
    )

    assert response.status_code == 302
    assert response.url == output.url


def test_tracking_uses_cache_subject_fallback_and_api_error(client, monkeypatch):
    """
    Expected behavior: tracking uses cache subject fallback and API error.
    """
    calls = []
    campaigns = SimpleNamespace(
        get=lambda campaign_id: (
            calls.append(campaign_id)
            or {"settings": {"title": "", "subject_line": "Monthly Evidence"}}
        )
    )
    mailchimp = SimpleNamespace(set_config=lambda config: None, campaigns=campaigns)
    monkeypatch.setattr(views.mailchimp_marketing, "Client", lambda: mailchimp)
    sent = []
    monkeypatch.setattr(views, "send_event", lambda *args: sent.append(args))

    client.get(reverse("open_view"), {"campaign": "cached"})
    client.get(reverse("open_view"), {"campaign": "cached"})

    assert calls == ["cached"]
    assert sent[-1][-1]["campaign"] == "monthly-evidence"

    failing = SimpleNamespace(
        set_config=lambda config: None,
        campaigns=SimpleNamespace(
            get=lambda campaign_id: (_ for _ in ()).throw(ApiClientError("bad"))
        ),
    )
    monkeypatch.setattr(views.mailchimp_marketing, "Client", lambda: failing)
    client.get(reverse("open_view"), {"campaign": "unavailable"})
    assert sent[-1][-1]["campaign"] == "unavailable"


def test_send_event_rejects_invalid_generated_client_id(monkeypatch):
    """
    Expected behavior: send event rejects invalid generated client id.
    """
    monkeypatch.setattr(views.re, "match", lambda pattern, value: None)

    with pytest.raises(Exception, match="client_id is not in the correct format"):
        views.send_event("measurement", "secret", "open", {})


def test_stringprint_archive_imports_hero_and_thumbnail(monkeypatch):
    """
    Expected behavior: stringprint archive imports hero and thumbnail.
    """
    item = create_research_item(slug="illustrated")
    archive = zip_bytes(
        {
            "hero.png": b"hero-image",
            "illustrated-thumbnail.png": b"thumbnail-image",
        }
    )
    item.zip_archive.save(
        "illustrated.zip", SimpleUploadedFile("illustrated.zip", archive)
    )
    monkeypatch.setattr(item, "create_search_items", lambda: None)

    item.unpack_archive()

    item.refresh_from_db()
    assert item.hero.read() == b"hero-image"
    assert item.thumbnail.read() == b"thumbnail-image"


def test_stringprint_search_file_url_and_http_error(monkeypatch, capsys):
    """
    Expected behavior: stringprint search file URL and HTTP error.
    """
    from urllib import request

    from repository.search_funcs import get_stringprint_search_data

    javascript = b'var tipuesearch = {"pages": [{"title": "", "text": "Text", "url": "index.html#intro"}]};'
    fetched = []
    monkeypatch.setattr(
        "repository.search_funcs.request.urlopen",
        lambda url: fetched.append(url) or SimpleNamespace(read=lambda: javascript),
    )

    result = get_stringprint_search_data(
        "https://research.mysociety.org/report/index.html", "Report"
    )

    assert fetched == ["https://research.mysociety.org/report/tipuesearch_content.js"]
    assert result[0].url.endswith("index.html#intro")

    monkeypatch.setattr(
        "repository.search_funcs.request.urlopen",
        lambda url: (_ for _ in ()).throw(
            request.HTTPError(url, 404, "missing", None, None)
        ),
    )
    assert get_stringprint_search_data("https://example.com/report/", "Report") == []
    assert "Cannot fetch info" in capsys.readouterr().out


def test_thumbnail_creator_uses_deployment_font_path(monkeypatch, tmp_path):
    """
    Expected behavior: thumbnail creator uses deployment font path.
    """
    source = tmp_path / "hero.png"
    Image.new("RGB", (220, 220), color=(20, 80, 160)).save(source)
    monkeypatch.setattr(
        "repository.image_processor.ColorThief",
        lambda path: SimpleNamespace(get_palette=lambda color_count: [(20, 80, 160)]),
    )
    real_exists = Path.exists
    monkeypatch.setattr(
        "repository.image_processor.os.path.exists",
        lambda path: (
            path == "/data/vhost/research.mysociety.org/research-repository"
            or real_exists(Path(path))
        ),
    )
    font_paths = []
    default_font = ImageFont.load_default()
    monkeypatch.setattr(
        "repository.image_processor.ImageFont.truetype",
        lambda path, size: font_paths.append(path) or default_font,
    )

    ThumbNailCreator.convert_hero_image_to_thumbnail(source, text="B")

    assert font_paths[0].startswith(
        "/data/vhost/research.mysociety.org/research-repository/"
    )


def test_noop_model_and_admin_branches(monkeypatch):
    """
    Expected behavior: noop model and admin branches.
    """
    person = create_person(institution="", link_behaviour="none", url="")
    monkeypatch.setattr(person, "absolute_url", lambda: None)
    data = person.json_ld_representation()
    assert "affiliation" not in data
    assert data["sameAs"] == []

    item = create_research_item(licence="", licencing=None, generate_thumbnail="")
    item.clean()
    item.migrate_licence()
    assert item.licencing is None

    request = RequestFactory().post("/admin/")
    item_calls = []
    monkeypatch.setattr(item, "fetch_toc", lambda save: item_calls.append("toc"))
    monkeypatch.setattr(
        item, "create_search_items", lambda: item_calls.append("search")
    )
    repository_admin.ResearchItemAdmin(ResearchItem, admin.site).save_model(
        request, item, SimpleNamespace(changed_data=[]), False
    )
    assert item_calls == ["toc", "search"]

    tag = create_tag(generate_thumbnail="", thumbnail=None)
    repository_admin.TagItemAdmin(type(tag), admin.site).save_model(
        request, tag, SimpleNamespace(changed_data=[]), False
    )

    minisite = create_mini_site()
    unpacked = []
    monkeypatch.setattr(minisite, "unpack_archive", lambda: unpacked.append(True))
    pages_admin.MiniSiteAdmin(MiniSite, admin.site).save_model(
        request, minisite, SimpleNamespace(changed_data=[]), False
    )
    assert unpacked == []


def test_home_without_shadow_group_and_snippet_text_true(client, monkeypatch):
    """
    Expected behavior: home without shadow group and snippet text true.
    """
    create_site()
    tag = create_tag(label="No shadow", front_page_order=1)
    item = create_research_item(featured=True, tags=[tag])
    monkeypatch.setattr("pages.views.FeedCache.fetch_feed", lambda: iter([]))

    home = client.get(reverse("home"))
    snippet = client.get(reverse("embed", args=[f"{tag.slug}/text:yes"]))

    assert home.context["featured_groups"] == [(tag, [item])]
    assert snippet.context["display_text"] is True


def test_populate_superuser_creation_is_idempotent():
    """
    Expected behavior: populate superuser creation is idempotent.
    """
    from repository.populate import create_super_user

    create_super_user()
    create_super_user()

    assert get_user_model().objects.filter(username="admin").count() == 1


def test_snippet_ignores_empty_option_segments():
    """
    Expected behavior: snippet ignores empty option segments.
    """
    request = RequestFactory().get("/embed/")
    response = views.snippet_view(request, "/featured/")

    assert response.status_code == 200


def test_tag_year_grouping_handles_long_runs_and_busy_years():
    """
    Expected behavior: tag year grouping handles long runs and busy years.
    """
    single_years = create_tag()
    create_research_item(date=date(2021, 1, 1), tags=[single_years])
    create_research_item(date=date(2022, 1, 1), tags=[single_years])
    create_research_item(date=date(2023, 1, 1), tags=[single_years])
    view = views.TagView()
    view.kwargs = {"slug1": single_years.slug}
    result = view.get_object()
    assert len(result.selected_items) == 3

    busy_year = create_tag()
    create_research_item(date=date(2021, 1, 1), tags=[busy_year])
    create_research_item(date=date(2021, 6, 1), tags=[busy_year])
    create_research_item(date=date(2022, 1, 1), tags=[busy_year])
    view = views.TagView()
    view.kwargs = {"slug1": busy_year.slug}
    result = view.get_object()
    assert [item.grouped_year for item in result.selected_items] == [
        "2022",
        "2021",
        "2021",
    ]


def test_base_settings_development_and_admin_branches(monkeypatch):
    """
    Expected behavior: base settings development and admin branches.
    """
    import runpy

    from conf import config

    monkeypatch.setattr(config, "STAGING", "0")
    monkeypatch.delattr(config, "ADMIN_NAME", raising=False)
    monkeypatch.delattr(config, "ADMIN_EMAIL", raising=False)
    settings_path = Path(__file__).parents[1] / "repository" / "settings" / "base.py"
    run_name = "repository.settings._branch_test"
    production = runpy.run_path(str(settings_path), run_name=run_name)
    assert production["ADMINS"] == ()
    assert "EMAIL_HOST" not in production

    monkeypatch.setattr(config, "STAGING", "1")
    monkeypatch.setattr(config, "ADMIN_NAME", "Research Admin", raising=False)
    monkeypatch.setattr(config, "ADMIN_EMAIL", "admin@example.com", raising=False)
    development = runpy.run_path(str(settings_path), run_name=run_name)
    assert development["ADMINS"] == (("Research Admin", "admin@example.com"),)
    assert development["EMAIL_HOST"] == "127.0.0.1"
