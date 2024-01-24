from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()
from ...models import Event


class Command(BaseCommand):
    help = 'seed database for development'

    def handle(self, *args, **options):
        # execute seed command
        self.stdout.write('deleting data...')
        self.delete_all()
        self.stdout.write('done')
        self.stdout.write('seeding data...')
        self.seed()
        self.stdout.write('done')

    def delete_all(self):
        """delete all events in database"""
        Event.objects.all().delete()
        User.objects.all().delete()

    def seed(self):
        """Seeds the database"""
        # define 5 events
        
        users = [
            {'username': 'testuser', 'password': 'testusertestuser'},
            {'username': 'testuser2', 'password': '1X<ISRUkw+tuK'},
            {'username': 'testuser3', 'password': '1X<ISRUkw+tuK'},
            {'username': 'testuser4', 'password': '1X<ISRUkw+tuK'},
            {'username': 'testuser5', 'password': '1X<ISRUkw+tuK'},
        ]

        for user in users:
            User.objects.create_user(username=user['username'], password=user['password'])


        events = [
            [User.objects.all()[0], 'event in the future', 'something futuristic', '2027-01-01T10:11:12Z', 'future'],
            [User.objects.all()[0], 'For Admins', 'only for admins really', '2023-12-25T02:59:39Z', 'Shinagawa'],
            [User.objects.all()[0], 'Very important event', 'Secret!', '2023-12-31T00:00:00Z', 'Shibuya'],
            [User.objects.all()[0], 'Normal Event', 'About something very normal', '2023-12-27T00:00:00Z', 'Ikebukuro'],
            [User.objects.all()[0], 'New Admin celebration', 'We gonna celebrate new admin', '2024-01-01T10:10:10Z', 'Here'],
        ]


        for event in events:
            e = Event.objects.create(
                title=event[1],
                details=event[2],
                date=event[3],
                location=event[4],
                creator=event[0],
            )
            e.attendees.add(event[0])
    
