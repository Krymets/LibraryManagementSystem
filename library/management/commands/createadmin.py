from django.core.management.base import BaseCommand
from library.models import User

class Command(BaseCommand):
    help = 'Create admin user with is_admin=True'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@example.com'
        password = 'password123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return

        admin = User.objects.create_user(username=username, email=email, password=password)
        admin.is_admin = True
        admin.save()

        self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created with password "{password}"'))
