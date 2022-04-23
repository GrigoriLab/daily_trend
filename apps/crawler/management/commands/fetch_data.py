from django.core.management.base import BaseCommand

from apps.crawler.tasks import fetch_trends


class Command(BaseCommand):
    help = "Fetch data from Google Trends and store it in the DB."

    def handle(self, *args, **options):
        fetch_trends()
