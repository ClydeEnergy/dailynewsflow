from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from news.models import Country, NewsProvider, NewsArticle
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample data for testing Daily News Flow'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))
        
        # Create countries
        countries_data = [
            {'name': 'United States', 'code': 'us'},
            {'name': 'United Kingdom', 'code': 'gb'},
            {'name': 'Canada', 'code': 'ca'},
            {'name': 'Australia', 'code': 'au'},
            {'name': 'Germany', 'code': 'de'},
            {'name': 'France', 'code': 'fr'},
            {'name': 'Japan', 'code': 'jp'},
            {'name': 'India', 'code': 'in'},
            {'name': 'Brazil', 'code': 'br'},
            {'name': 'South Africa', 'code': 'za'},
        ]
        
        countries = []
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults={
                    'name': country_data['name'],
                    'is_active': True
                }
            )
            countries.append(country)
            if created:
                self.stdout.write(f'Created country: {country.name}')

        # Create news providers
        providers_data = [
            {
                'name': 'BBC News',
                'website': 'https://www.bbc.com/news',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/BBC_News_2019.svg/1200px-BBC_News_2019.svg.png'
            },
            {
                'name': 'CNN',
                'website': 'https://www.cnn.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/CNN.svg/1200px-CNN.svg.png'
            },
            {
                'name': 'Reuters',
                'website': 'https://www.reuters.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Reuters_Logo.svg/1200px-Reuters_Logo.svg.png'
            },
            {
                'name': 'Associated Press',
                'website': 'https://apnews.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Associated_Press_logo_2012.svg/1200px-Associated_Press_logo_2012.svg.png'
            },
            {
                'name': 'The Guardian',
                'website': 'https://www.theguardian.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/The_Guardian.svg/1200px-The_Guardian.svg.png'
            },
            {
                'name': 'New York Times',
                'website': 'https://www.nytimes.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/New_York_Times_logo_variation.jpg/1200px-New_York_Times_logo_variation.jpg'
            },
            {
                'name': 'Al Jazeera',
                'website': 'https://www.aljazeera.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Al_Jazeera_English_newlogo.svg/1200px-Al_Jazeera_English_newlogo.svg.png'
            },
            {
                'name': 'Deutsche Welle',
                'website': 'https://www.dw.com',
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Deutsche_Welle_symbol_2012.svg/1200px-Deutsche_Welle_symbol_2012.svg.png'
            },
        ]
        
        providers = []
        for provider_data in providers_data:
            provider, created = NewsProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults={
                    'website': provider_data['website'],
                    'logo_url': provider_data.get('logo_url', ''),
                    'is_active': True
                }
            )
            providers.append(provider)
            if created:
                self.stdout.write(f'Created news provider: {provider.name}')

        # Create sample news articles
        sample_articles = [
            {
                'title': 'Global Climate Summit Reaches Historic Agreement',
                'description': 'World leaders have reached a landmark agreement on climate action at the international summit, setting ambitious targets for carbon reduction.',
                'image': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e5?w=800&h=600&fit=crop',
            },
            {
                'title': 'Technology Breakthrough in Renewable Energy',
                'description': 'Scientists announce a major breakthrough in solar panel efficiency, potentially revolutionizing clean energy production worldwide.',
                'image': 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&h=600&fit=crop',
            },
            {
                'title': 'International Space Station Mission Success',
                'description': 'The latest mission to the International Space Station has achieved all its objectives, advancing scientific research in space.',
                'image': 'https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800&h=600&fit=crop',
            },
            {
                'title': 'Economic Markets Show Strong Recovery',
                'description': 'Global financial markets demonstrate resilience with strong performance across major indices, signaling economic recovery.',
                'image': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop',
            },
            {
                'title': 'Medical Research Breakthrough in Treatment',
                'description': 'Researchers announce significant progress in developing new treatment methods, offering hope for millions of patients worldwide.',
                'image': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop',
            },
            {
                'title': 'Cultural Festival Celebrates International Unity',
                'description': 'A massive cultural festival brings together artists and performers from around the world, celebrating diversity and unity.',
                'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&h=600&fit=crop',
            },
            {
                'title': 'Sports Championship Breaks Attendance Records',
                'description': 'The international championship event sets new attendance records, showcasing outstanding athletic performances.',
                'image': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=600&fit=crop',
            },
            {
                'title': 'Educational Initiative Transforms Learning',
                'description': 'A groundbreaking educational program demonstrates remarkable success in improving student outcomes across multiple regions.',
                'image': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=600&fit=crop',
            },
            {
                'title': 'Environmental Conservation Project Expands',
                'description': 'Major conservation efforts show positive results as protected areas expand and wildlife populations begin to recover.',
                'image': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop',
            },
            {
                'title': 'Innovation in Transportation Technology',
                'description': 'New developments in sustainable transportation offer promising solutions for urban mobility and environmental concerns.',
                'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
            },
        ]

        # Create articles with random combinations
        for i, article_data in enumerate(sample_articles):
            # Create multiple variations with different countries and providers
            for j in range(3):  # Create 3 variations of each article
                country = random.choice(countries)
                provider = random.choice(providers)
                
                # Add variation to title
                varied_title = f"{article_data['title']} - {country.name} Report"
                
                # Create article
                article, created = NewsArticle.objects.get_or_create(
                    title=varied_title,
                    country=country,
                    news_provider=provider,
                    defaults={
                        'description': article_data['description'],
                        'image': article_data['image'],
                        'link': f"{provider.website}/article-{i}-{j}",
                        'date_posted': timezone.now() - timedelta(
                            days=random.randint(0, 30),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59)
                        ),
                        'views': random.randint(50, 5000),
                        'is_active': True,
                    }
                )
                
                if created:
                    self.stdout.write(f'Created article: {varied_title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Sample data loaded successfully!\n'
                f'Countries: {len(countries)}\n'
                f'Providers: {len(providers)}\n'
                f'Articles: {NewsArticle.objects.count()}'
            )
        )
