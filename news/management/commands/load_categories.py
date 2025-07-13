from django.core.management.base import BaseCommand
from django.utils.text import slugify
from news.models import Category


class Command(BaseCommand):
    help = 'Load sample categories'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Politics',
                'description': 'Political news and government affairs',
                'icon': 'fas fa-landmark',
                'color': '#dc3545'
            },
            {
                'name': 'Business',
                'description': 'Business news, economics, and finance',
                'icon': 'fas fa-briefcase',
                'color': '#007bff'
            },
            {
                'name': 'Technology',
                'description': 'Technology news and innovations',
                'icon': 'fas fa-laptop',
                'color': '#28a745'
            },
            {
                'name': 'Sports',
                'description': 'Sports news and events',
                'icon': 'fas fa-football-ball',
                'color': '#fd7e14'
            },
            {
                'name': 'Health',
                'description': 'Health and medical news',
                'icon': 'fas fa-heart',
                'color': '#e83e8c'
            },
            {
                'name': 'Entertainment',
                'description': 'Entertainment and celebrity news',
                'icon': 'fas fa-film',
                'color': '#6f42c1'
            },
            {
                'name': 'World',
                'description': 'International and world news',
                'icon': 'fas fa-globe',
                'color': '#20c997'
            },
            {
                'name': 'Science',
                'description': 'Science and research news',
                'icon': 'fas fa-flask',
                'color': '#17a2b8'
            },
        ]

        created_count = 0

        for category_data in categories_data:
            category_data['slug'] = slugify(category_data['name'])
            
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories!')
        )
