import pytest

from pages.views import FeedCache
from repository import views

from .fixtures import create_site, reset_fixture_sequences


@pytest.fixture(autouse=True)
def isolate_process_state(settings, tmp_path):
    """Keep storage, indexes, and module-level caches local to each test."""
    reset_fixture_sequences()
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.ZIP_ROOT = tmp_path / "zip"
    settings.SITES_ROOT = tmp_path / "sites"

    FeedCache._feed = []
    FeedCache._time = None
    views.campaign_tracking_cache.clear()
    yield
    FeedCache._feed = []
    FeedCache._time = None
    views.campaign_tracking_cache.clear()


@pytest.fixture
def site(db):
    """Provide the singleton-style site configuration expected by views."""
    return create_site()
