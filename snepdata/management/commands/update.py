from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update db with current snep certifications'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Command launched'))