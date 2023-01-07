from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

#this is strictly to test, these should be env variables to protect them from public
class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "alex.provenzano87@gmail.com", "panthers12@")