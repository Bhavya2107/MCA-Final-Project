from django.core.management.base import BaseCommand
from new_laptops.models import LaptopCategory


class Command(BaseCommand):
    help = 'Populate laptop categories with predefined options'

    def handle(self, *args, **options):
        categories = [
            'Ultrabooks',
            'Gaming Laptops',
            '2-in-1 Convertibles',
            'Professional Workstations',
            'Chromebooks',
            'Rugged Laptops',
        ]

        created_count = 0
        updated_count = 0

        for category_name in categories:
            category, created = LaptopCategory.objects.get_or_create(
                name=category_name,
                defaults={'name': category_name}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(categories)} categories. '
                f'Created: {created_count}, Already existed: {updated_count}'
            )
        )