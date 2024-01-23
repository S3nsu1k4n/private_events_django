from django.core.management.base import BaseCommand
from ...models import Event


class Command(BaseCommand):
    help = 'seed database for development'

    def handle(self, *args, **options):
        # execute seed command
        self.stdout.write('seeding data...')
        self.delete_all()
        self.seed()
        self.stdout.write('done')

    def delete_all(self):
        """delete all events in database"""
        Event.objects.all().delete()

    def seed(self):
        """Seeds the database"""
        # define 5 events
        events = [
            ['admin', 'event in the future', 'something futuristic', '2027-01-01 10:11:12', 'future'],
            ['admin', 'For Admins', 'only for admins really', '2023-12-25 02:59:39', 'Shinagawa'],
            ['admin', 'Very important event', 'Secret!', '2023-12-31 00:00:00', 'Shibuya'],
            ['testuser1', 'Normal Event', 'About something very normal', '2023-12-27 00:00:00', 'Ikebukuro'],
            ['admin', 'New Admin celebration', 'We gonna celebrate new admin', '2024-01-01 10:10:10', 'Here'],
        ]
