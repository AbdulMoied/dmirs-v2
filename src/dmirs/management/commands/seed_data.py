# your_app/management/commands/composite_command.py
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'seed_data_base'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('*** Seed process started. ***'))

        # Seed  Data Files
        self.stdout.write(self.style.SUCCESS('Seeding Data Files'))
        call_command('data_file_seed')
        # Seed headers with code
        self.stdout.write(self.style.SUCCESS('Seeding Headers'))
        call_command('header_seed')

        # Add more commands as needed
        self.stdout.write(self.style.SUCCESS('*** Seed Complete. ***'))