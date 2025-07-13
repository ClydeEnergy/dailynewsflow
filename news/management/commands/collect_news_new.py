import requests
import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from news.models import NewsArticle, NewsProvider, Country

logger = logging.getLogger('news')


class Command(BaseCommand):
    help = 'Collect news from various news providers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            type=str,
            help='Specific provider to collect from',
        )
        parser.add_argument(
            '--country',
            type=str,
            help='Specific country to collect for',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of articles to collect per provider',
        )

    def handle(self, *args, **options):
        """Main handler for the collect news command"""
        start_time = timezone.now()
        self.stdout.write("Starting news collection...")

        # Get active providers and countries
        providers = NewsProvider.objects.filter(is_active=True)
        countries = Country.objects.filter(is_active=True)

        # Filter by command line options
        if options['provider']:
            providers = providers.filter(name__icontains=options['provider'])
        
        if options['country']:
            countries = countries.filter(code__iexact=options['country'])

        total_collected = 0
        total_updated = 0

        for provider in providers:
            for country in countries:
                self.stdout.write(f"Collecting from {provider.name} for {country.name}...")
                
                collected, updated = self.collect_from_provider(
                    provider, country, options['limit']
                )
                
                total_collected += collected
                total_updated += updated
                
                self.stdout.write(
                    f"  → Collected: {collected}, Updated: {updated}"
                )

        duration = timezone.now() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Collection completed in {duration.total_seconds():.2f} seconds. "
                f"Total collected: {total_collected}, Updated: {total_updated}"
            )
        )

    def collect_from_provider(self, provider, country, limit):
        """Collect news from a specific provider for a country"""
        
        collected = 0
        updated = 0
        
        try:
            # Simulate collecting news (you can replace this with actual API calls)
            # For now, this is just a placeholder implementation
            self.stdout.write(f"Simulating collection from {provider.name} for {country.name}")
            
            # Example: Create some sample articles
            sample_articles = [
                {
                    'title': f'Breaking News from {country.name} - {timezone.now().strftime("%Y-%m-%d %H:%M")}',
                    'description': f'This is a sample news article from {provider.name} about events in {country.name}.',
                    'image': 'https://via.placeholder.com/400x200',
                    'link': f'{provider.website}/sample-article-{timezone.now().strftime("%Y%m%d%H%M")}',
                }
            ]
            
            for article_data in sample_articles[:limit]:
                # Check if article already exists
                existing = NewsArticle.objects.filter(
                    title=article_data['title'],
                    news_provider=provider,
                    country=country
                ).first()
                
                if existing:
                    # Update existing article
                    existing.description = article_data['description']
                    existing.updated_at = timezone.now()
                    existing.save()
                    updated += 1
                else:
                    # Create new article
                    NewsArticle.objects.create(
                        title=article_data['title'],
                        description=article_data['description'],
                        country=country,
                        news_provider=provider,
                        image=article_data['image'],
                        link=article_data['link'],
                        date_posted=timezone.now(),
                        is_active=True,
                    )
                    collected += 1
            
            return collected, updated
            
        except Exception as e:
            logger.error(f"Error collecting from {provider.name}: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f"Error: {str(e)}")
            )
            return 0, 0

    def get_newsapi_articles(self, provider, country, limit):
        """Get articles from NewsAPI (example implementation)"""
        # This is just a placeholder for actual NewsAPI integration
        # You would need to implement actual API calls here
        return []

    def get_guardian_articles(self, provider, country, limit):
        """Get articles from Guardian API (example implementation)"""
        # This is just a placeholder for actual Guardian API integration
        # You would need to implement actual API calls here
        return []

    def create_or_update_article(self, article_data, provider, country):
        """Create or update a news article"""
        try:
            # Check if article already exists
            existing = NewsArticle.objects.filter(
                title=article_data['title'],
                news_provider=provider,
                country=country
            ).first()

            if existing:
                # Update existing article
                existing.description = article_data.get('description', existing.description)
                existing.image = article_data.get('image', existing.image)
                existing.link = article_data.get('link', existing.link)
                existing.updated_at = timezone.now()
                existing.save()
                return False, True  # Not created, but updated

            else:
                # Create new article
                NewsArticle.objects.create(
                    title=article_data['title'],
                    description=article_data.get('description', ''),
                    country=country,
                    news_provider=provider,
                    image=article_data.get('image', ''),
                    link=article_data.get('link', ''),
                    date_posted=timezone.now(),
                    is_active=True,
                )
                return True, False  # Created, not updated

        except Exception as e:
            logger.error(f"Error creating/updating article: {str(e)}")
            return False, False
