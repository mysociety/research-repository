from django.core.management import BaseCommand
from repository.models import ResearchItem


class Command(BaseCommand):
    # Show this when the user types help
    help = "Update search database (for initial population)"

    # A command must define handle()
    def handle(self, *args, **options):
        for item in ResearchItem.objects.all():
            print(f"Updating search items for {item.title}")
            item.create_search_items()
