from django.core.management.base import BaseCommand
from django.utils.text import slugify
from user.models import Role

class Command(BaseCommand):
    help = 'Seed roles into the database'

    def handle(self, *args, **kwargs):
        roles_data = [
            {
                "name": "Admin",
                "permissions": {
                    "user": ["view", "add", "edit", "delete"],
                    "transaction": ["view", "add", "edit", "delete"],
                    "report": ["view"]
                },
            },
            {
                "name": "Staff",
                "permissions": {
                    "user": ["view", "add", "edit", "delete"],
                    "transaction": ["view", "add"],
                },
            },
            {
                "name": "Customer",
                "permissions": {
                    "user": ["view", "add", "edit", "delete"],
                    "transaction": ["view"],
                },
            },
        ]

        for data in roles_data:
            role, created = Role.objects.update_or_create(
                name=data["name"],
                defaults={
                    "permissions": data["permissions"],
                    "slug": slugify(data["name"])
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} role: {role.name}"))
