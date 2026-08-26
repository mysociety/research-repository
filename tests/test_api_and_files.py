"""
API authorization, archive extraction safety, image generation, and commands.
"""

import io
import json
import zipfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from pages.models import MiniSite
from repository.image_processor import (
    ThumbNailCreator,
    interestingness,
    make_positive,
    round_to,
)
from repository.models import ResearchItem, SearchItem

from .fixtures import (
    create_mini_site,
    create_research_item,
    create_research_licence,
)

pytestmark = pytest.mark.django_db


def zip_bytes(files):
    contents = io.BytesIO()
    with zipfile.ZipFile(contents, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    return contents.getvalue()


def authenticated_api_client(is_staff=True):
    user = get_user_model().objects.create_user(
        username="uploader", password="password", is_staff=is_staff
    )
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


def put_archive(client, path, filename="report.zip"):
    return client.put(
        path,
        zip_bytes({"index.html": "<h1>Report</h1>"}),
        content_type="application/zip",
        HTTP_CONTENT_DISPOSITION=f'attachment; filename="{filename}"',
    )


def test_item_upload_requires_authentication():
    """
    Expected behavior: item upload requires authentication.
    """
    response = put_archive(APIClient(), "/api/upload_zip/report")

    assert response.status_code == 401
    assert ResearchItem.objects.count() == 0


def test_item_upload_requires_staff_user():
    """
    Expected behavior: item upload requires staff user.
    """
    response = put_archive(
        authenticated_api_client(is_staff=False), "/api/upload_zip/report"
    )

    assert response.status_code == 403


def test_item_upload_creates_draft_and_unpacks(monkeypatch):
    """
    Expected behavior: item upload creates draft and unpacks.
    """
    unpacked = []
    monkeypatch.setattr(
        ResearchItem, "unpack_archive", lambda item: unpacked.append(item.slug)
    )

    response = put_archive(authenticated_api_client(), "/api/upload_zip/new-report")

    item = ResearchItem.objects.get(slug="new-report")
    assert response.status_code == 201
    assert response.json() == {"Message": "Upload Complete", "item_id": item.id}
    assert item.published is False
    assert item.zip_archive.name.endswith("report.zip")
    assert unpacked == ["new-report"]


def test_site_upload_rejects_unknown_slug():
    """
    Expected behavior: site upload rejects unknown slug.
    """
    response = put_archive(authenticated_api_client(), "/api/upload_site/unknown/")

    assert response.status_code == 400
    assert response.json() == {"Message": "Slug does not match item"}


def test_site_upload_passes_preserve_existing_flag(monkeypatch):
    """
    Expected behavior: site upload passes preserve existing flag.
    """
    site = create_mini_site(slug="tool")
    calls = []
    monkeypatch.setattr(
        MiniSite,
        "unpack_archive",
        lambda item, preserve_existing=False: calls.append(preserve_existing),
    )
    client = authenticated_api_client()

    normal = put_archive(client, f"/api/upload_site/{site.slug}/")
    preserved = put_archive(client, f"/api/upload_site/{site.slug}/yes")

    assert normal.status_code == preserved.status_code == 201
    assert calls == [False, True]


def test_minisite_unpack_replaces_or_preserves_existing_files(settings):
    """
    Expected behavior: minisite unpack replaces or preserves existing files.
    """
    site = create_mini_site(site_folder="tool")
    destination = Path(settings.SITES_ROOT) / site.site_folder
    destination.mkdir(parents=True)
    existing = destination / "existing.txt"
    existing.write_text("keep me")
    site.zip_archive.save(
        "tool.zip",
        SimpleUploadedFile("tool.zip", zip_bytes({"new.txt": "new"})),
    )

    site.unpack_archive(preserve_existing=True)
    assert existing.exists()
    assert (destination / "new.txt").read_text() == "new"

    site.zip_archive.save(
        "tool.zip",
        SimpleUploadedFile("tool.zip", zip_bytes({"replacement.txt": "replacement"})),
    )
    site.unpack_archive(preserve_existing=False)
    assert not existing.exists()
    assert (destination / "replacement.txt").read_text() == "replacement"
    site.refresh_from_db()
    assert site.last_update is not None


def test_minisite_archive_cannot_write_outside_destination(settings):
    """
    Expected behavior: minisite archive cannot write outside destination.
    """
    site = create_mini_site(site_folder="tool")
    site.zip_archive.save(
        "tool.zip",
        SimpleUploadedFile("tool.zip", zip_bytes({"../escaped.txt": "unsafe"})),
    )

    site.unpack_archive()

    assert not (Path(settings.SITES_ROOT) / "escaped.txt").exists()


def test_research_archive_populates_metadata_authors_and_outputs(settings, monkeypatch):
    """
    Expected behavior: research archive populates metadata authors and outputs.
    """
    create_research_licence(slug="cc-by-4.0", name="CC BY 4.0")
    metadata = {
        "title": "Imported title",
        "publish_date": "2023-05-06",
        "description": "Imported abstract",
        "authors": "Ada Lovelace,Grace Hopper",
    }
    archive = zip_bytes(
        {
            "index.html": "<h1>Report</h1>",
            "plain.html": "Report text",
            "report.pdf": b"pdf",
            "settings-for-render.json": json.dumps(metadata),
        }
    )
    item = create_research_item(slug="report")
    item.zip_archive.save("report.zip", SimpleUploadedFile("report.zip", archive))
    searched = []
    monkeypatch.setattr(
        ResearchItem, "create_search_items", lambda obj: searched.append(obj.pk)
    )

    item.unpack_archive()

    item.refresh_from_db()
    assert [person.full_name() for person in item.author_list()] == [
        "Ada Lovelace",
        "Grace Hopper",
    ]
    assert set(item.outputs.values_list("title", flat=True)) == {
        "Read Online",
        "Plain Text",
        "PDF",
    }
    assert searched == [item.pk]
    assert (Path(settings.ZIP_ROOT) / "report" / "index.html").exists()


def test_research_archive_without_metadata_still_unpacks(monkeypatch):
    """
    Expected behavior: research archive without metadata still unpacks.
    """
    item = create_research_item()
    archive = zip_bytes({"index.html": "<h1>Report</h1>"})
    item.zip_archive.save("minimal.zip", SimpleUploadedFile("minimal.zip", archive))
    monkeypatch.setattr(ResearchItem, "create_search_items", lambda obj: None)

    item.unpack_archive()

    assert item.outputs.filter(title="Read Online").exists()


def test_research_archive_without_index_does_not_create_read_online(monkeypatch):
    """
    Expected behavior: research archive without index does not create read online.
    """
    metadata = {"authors": ""}
    item = create_research_item()
    archive = zip_bytes({"settings-for-render.json": json.dumps(metadata)})
    item.zip_archive.save("no-index.zip", SimpleUploadedFile("no-index.zip", archive))
    monkeypatch.setattr(ResearchItem, "create_search_items", lambda obj: None)

    item.unpack_archive()

    assert not item.outputs.filter(title="Read Online").exists()


def test_image_color_helpers():
    """
    Expected behavior: image color helpers.
    """
    assert round_to(24, 10) == 20
    assert make_positive(-4) == 4
    assert make_positive(4) == 4
    assert interestingness((100, 100, 100)) == 0
    assert interestingness((250, 10, 10)) > 0
    assert ThumbNailCreator.color_distance((0, 0, 0), (0, 0, 0)) == 0
    assert ThumbNailCreator.color_distance((0, 0, 0), (255, 255, 255)) > 0


def test_thumbnail_creator_returns_expected_png(monkeypatch, tmp_path):
    """
    Expected behavior: thumbnail creator returns expected PNG.
    """
    from PIL import Image, ImageFont

    source = tmp_path / "hero.png"
    Image.new("RGB", (220, 220), color=(20, 80, 160)).save(source)
    monkeypatch.setattr(
        "repository.image_processor.ColorThief",
        lambda path: type(
            "Palette", (), {"get_palette": lambda self, color_count: [(20, 80, 160)]}
        )(),
    )
    default_font = ImageFont.load_default()
    monkeypatch.setattr(
        "repository.image_processor.ImageFont.truetype",
        lambda path, size: default_font,
    )

    result = ThumbNailCreator.convert_hero_image_to_thumbnail(source, text="B")
    generated = Image.open(result)

    assert generated.format == "PNG"
    assert generated.size == (110, 150)


def test_update_search_command_only_refreshes_missing_items_with_update(monkeypatch):
    """
    Expected behavior: update search command only refreshes missing items with update.
    """
    missing = create_research_item(title="Missing search")
    existing = create_research_item(title="Existing search")
    draft = create_research_item(title="Draft", published=False)
    SearchItem.objects.create(
        research_item=existing, title="Indexed", url="/indexed", text="Indexed"
    )
    called = []
    monkeypatch.setattr(
        ResearchItem, "create_search_items", lambda item: called.append(item)
    )

    call_command("update_search", update=True)

    assert called == [missing]
    assert draft not in called


def test_update_search_command_continues_after_item_failure(monkeypatch, capsys):
    """
    Expected behavior: update search command continues after item failure.
    """
    first = create_research_item(title="First")
    second = create_research_item(title="Second")
    called = []

    def update(item):
        called.append(item)
        if item == first:
            raise RuntimeError("search unavailable")

    monkeypatch.setattr(ResearchItem, "create_search_items", update)

    call_command("update_search", update=False)

    assert set(called) == {first, second}
    assert "Error updating search items for First" in capsys.readouterr().out


def test_populate_command_delegates(monkeypatch):
    """
    Expected behavior: populate command delegates.
    """
    called = []
    monkeypatch.setattr(
        "repository.management.commands.populate.populate", lambda: called.append(True)
    )

    call_command("populate")

    assert called == [True]


def test_populate_builds_representative_development_dataset(monkeypatch):
    """
    Expected behavior: populate builds representative development dataset.
    """
    from pages.models import Page
    from repository import populate as population
    from repository.models import ResearchOutput, Tag

    monkeypatch.setattr(ResearchItem, "create_search_items", lambda item: None)
    population.random.seed(1)

    population.populate()

    assert get_user_model().objects.filter(username="admin", is_superuser=True).exists()
    assert Tag.objects.filter(slug="hidden", display=False).exists()
    assert Page.objects.filter(slug="test_page").exists()
    assert ResearchItem.objects.count() == 20
    assert ResearchOutput.objects.count() >= 20
