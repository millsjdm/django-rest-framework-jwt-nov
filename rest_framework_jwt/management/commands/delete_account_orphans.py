import json

from django.core.management.base import BaseCommand

from rest_framework_jwt.models import User
from rest_framework_jwt.tasks import delete_account_from_username


class Command(BaseCommand):
    help = "Delete orphans from Auth0 Export."

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='?',
            default='barberscore.json',
        )

    def handle(self, *args, **options):
        # Parse URL input
        filename = options['filename']
        accounts = []
        self.stdout.write("Getting Accounts from {0}...".format(filename))

        with open(filename) as file:
            for line in file:
                item = json.loads(line)
                accounts.append(item['Id'])
        self.stdout.write("Getting Users...")
        users = User.objects.filter(
            id__startswith='auth0|',
        ).values_list(
            'id',
            flat=True,
        )
        users_set = set(users)
        self.stdout.write("Finding Orphans...")
        orphans = [item for item in accounts if item not in users_set]
        t = len(orphans)
        i = 0
        for orphan in orphans:
            i += 1
            self.stdout.flush()
            self.stdout.write("Deleting {0} of {1} Orphans...".format(i, t), ending='\r')
            delete_account_from_username.delay(orphan)
        self.stdout.write("")
        self.stdout.write("Deleted {0} Orphans.".format(t))
        self.stdout.write("Complete.")
        return
