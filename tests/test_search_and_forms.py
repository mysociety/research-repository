"""
Search extraction and indexing plus blog-import form workflows.
"""

import json
from types import SimpleNamespace

import pytest

from repository.forms import BlogImport
from repository.models import ResearchItem, SearchItem
from repository.search_funcs import (
    PhraseHighlighter,
    SearchData,
    get_data_from_mysociety_blog,
    get_stringprint_search_data,
)

from .fixtures import create_research_item, create_research_output, create_tag

pytestmark = pytest.mark.django_db


def response_with(content):
    return SimpleNamespace(read=lambda: content)


def test_blog_search_extracts_nonempty_paragraphs_and_deep_links(monkeypatch):
    """
    Expected behavior: blog search extracts nonempty paragraphs and deep links.
    """
    html = b"""
        <div class="wordpress-editor-content">
          <p>One useful paragraph.</p><p> </p><p>Another point</p>
        </div>
    """
    monkeypatch.setattr(
        "repository.search_funcs.request.urlopen", lambda url: response_with(html)
    )

    results = get_data_from_mysociety_blog("https://mysociety.org/post", "Post")

    assert [result.text for result in results] == [
        "One useful paragraph.",
        "Another point",
    ]
    assert results[0].url.endswith("#:~:text=One%20useful%20paragraph.")
    assert all(result.title == "Post" for result in results)


def test_blog_search_skips_pdfs_and_pages_without_expected_content(monkeypatch):
    """
    Expected behavior: blog search skips pdfs and pages without expected content.
    """
    called = []
    monkeypatch.setattr(
        "repository.search_funcs.request.urlopen",
        lambda url: called.append(url) or response_with(b"<html></html>"),
    )

    assert get_data_from_mysociety_blog("https://example.com/file.pdf", "PDF") == []
    assert get_data_from_mysociety_blog("https://example.com/post", "Post") == []
    assert called == ["https://example.com/post"]


def test_stringprint_search_extracts_pages_and_builds_urls(monkeypatch):
    """
    Expected behavior: stringprint search extracts pages and builds urls.
    """
    source = {
        "pages": [
            {"title": "Chapter", "text": " Chapter text ", "url": "chapter.html"},
            {"title": "", "text": "Intro", "url": "index.html#intro"},
            {"title": "Empty", "text": " ", "url": "empty.html"},
        ]
    }
    javascript = b"var tipuesearch = " + json.dumps(source).encode() + b";"
    urls = []
    monkeypatch.setattr(
        "repository.search_funcs.request.urlopen",
        lambda url: urls.append(url) or response_with(javascript),
    )

    results = get_stringprint_search_data(
        "https://research.mysociety.org/report/", "Report"
    )

    assert urls == ["https://research.mysociety.org/report/tipuesearch_content.js"]
    assert results == [
        SearchData(
            url="https://research.mysociety.org/report/chapter.html",
            text="Chapter text",
            title="Report: Chapter",
        ),
        SearchData(
            url="https://research.mysociety.org/report/#intro",
            text="Intro",
            title="Report",
        ),
    ]


def test_phrase_highlighter_keeps_phrases_and_removes_operators():
    """
    Expected behavior: phrase highlighter keeps phrases and removes operators.
    """
    highlighter = PhraseHighlighter('"open data" AND councils OR NOT')

    assert "open data" in highlighter.query_words
    assert "and" not in highlighter.query_words
    assert "or" not in highlighter.query_words
    assert "not" not in highlighter.query_words


def test_create_search_items_replaces_old_data_and_truncates_title(monkeypatch):
    """
    Expected behavior: create search items replaces old data and truncates title.
    """
    item = create_research_item()
    create_research_output(
        research_item=item, url="https://www.mysociety.org/2024/post"
    )
    create_research_output(
        research_item=item, url="https://research.mysociety.org/report/"
    )
    create_research_output(research_item=item, url="https://example.com/ignored")
    SearchItem.objects.create(
        research_item=item, title="Old", url="/old", text="Old text"
    )
    monkeypatch.setattr(
        "repository.models.get_data_from_mysociety_blog",
        lambda url, title: [SearchData(url="/blog", text="Blog", title="B" * 300)],
    )
    monkeypatch.setattr(
        "repository.models.get_stringprint_search_data",
        lambda url, title: [SearchData(url="/report", text="Report", title="Report")],
    )

    item.create_search_items()

    assert list(item.search_items.values_list("url", "text")) == [
        ("/blog", "Blog"),
        ("/report", "Report"),
    ]
    assert item.search_items.get(url="/blog").title == "B" * 250 + "..."


def test_create_search_items_ignores_external_index_html(monkeypatch):
    """
    Expected behavior: create search items ignores external index html.
    """
    item = create_research_item()
    create_research_output(
        research_item=item, url="https://untrusted.example/index.html"
    )
    called = []
    monkeypatch.setattr(
        "repository.models.get_stringprint_search_data",
        lambda url, title: called.append(url) or [],
    )

    item.create_search_items()

    assert called == []


def test_fetch_toc_updates_cache_and_can_avoid_saving(monkeypatch):
    """
    Expected behavior: fetch TOC updates cache and can avoid saving.
    """
    item = create_research_item(table_of_contents_url="https://example.com/toc.json")
    monkeypatch.setattr(
        "repository.models.urllib.request.urlopen",
        lambda url: response_with(b'[{"name": "Intro", "children": []}]'),
    )

    item.fetch_toc(save=False)

    assert json.loads(item.table_of_contents_cache)[0]["name"] == "Intro"
    item.refresh_from_db()
    assert item.table_of_contents_cache == ""


def test_blog_import_creates_item_output_authors_and_tags(monkeypatch, tmp_path):
    """
    Expected behavior: blog import creates item output authors and tags.
    """
    tag = create_tag()
    html = b"""
      <meta property="og:title" content="Open Data Findings">
      <meta property="og:description" content="What we learned">
      <meta property="og:image" content="https://example.com/hero.png">
      <meta itemprop="author" content="Ada Lovelace">
    """
    image_path = tmp_path / "hero.png"
    image_path.write_bytes(b"not processed in this test")
    monkeypatch.setattr("repository.forms.urlopen", lambda url: response_with(html))
    monkeypatch.setattr(
        "repository.forms.urlretrieve", lambda url: (str(image_path), None)
    )
    thumbnails = []
    searches = []
    monkeypatch.setattr(
        ResearchItem,
        "generate_thumbnail_from_hero",
        lambda item: thumbnails.append(item.pk),
    )
    monkeypatch.setattr(
        ResearchItem, "create_search_items", lambda item: searches.append(item.pk)
    )
    form = BlogImport(
        data={
            "url": "https://example.com/post",
            "featured": True,
            "tags": [tag.pk],
        }
    )

    assert form.is_valid(), form.errors
    result = form.save()

    item = ResearchItem.objects.get(slug="open-data-findings")
    assert result == item.url()
    assert item.featured is True
    assert list(item.tags.all()) == [tag]
    assert item.outputs.get().url == "https://example.com/post"
    assert [person.full_name() for person in item.author_list()] == ["Ada Lovelace"]
    assert thumbnails == searches == [item.pk]


def test_search_index_only_includes_published_research():
    """
    Expected behavior: search index only includes published research.
    """
    from repository.search_indexes import NoteIndex

    published = create_research_item()
    draft = create_research_item(published=False)
    visible = SearchItem.objects.create(
        research_item=published, title="Visible", url="/visible", text="Text"
    )
    SearchItem.objects.create(
        research_item=draft, title="Draft", url="/draft", text="Text"
    )

    assert list(NoteIndex().index_queryset()) == [visible]
