from django.core.management import BaseCommand
from repository.models import ResearchItem

# add an optional parameter to the command for if a search should be updated if it already exists


class Command(BaseCommand):
    # Show this when the user types help
    help = "Update search database (for initial population)"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Do not refetch search data where already exists",
        )

    # A command must define handle()
    def handle(self, *args, **options):
        update = options["update"]
        for item in ResearchItem.objects.filter(published=True):
            # if either there are no search items, or where update is false, update the search items
            if not item.search_items.exists() or not update:
                try:
                    item.create_search_items()
                except Exception:
                    print(f"Error updating search items for {item.title}")
