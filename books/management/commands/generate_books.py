from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from books.models import Book
import random

class Command(BaseCommand):
    help = 'Generate 15 fake books associated with the first user in the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        # Fetch the first user in the database
        first_user = User.objects.first()
        if not first_user:
            self.stdout.write(self.style.ERROR("No users found. Please create a user first."))
            return

        # Create 15 fake books
        for _ in range(15):
            book = Book(
                title=fake.sentence(nb_words=5),
                author=fake.name(),
                published_date=fake.date_between(start_date="-10y", end_date="today"),
                isbn=1 + random.randint(0, 9999),
                pages=random.randint(100, 1000),
                cover=fake.image_url(),
                language=fake.language_name(),
                added_by=first_user
            )
            book.save()

        self.stdout.write(self.style.SUCCESS("15 fake books created successfully!"))
