from django.core.management import BaseCommand
from repository.populate import populate


class Command(BaseCommand):
    # Show this when the user types help
    help = "Populate with test data"

    # A command must define handle()
    def handle(self, *args, **options):
        populate()
