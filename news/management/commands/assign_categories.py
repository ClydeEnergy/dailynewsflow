from django.core.management.base import BaseCommand
from news.models import NewsArticle, Category
import random


class Command(BaseCommand):
    help = 'Assign categories to existing articles and create sample articles'

    def handle(self, *args, **options):
        categories = list(Category.objects.all())
        
        if not categories:
            self.stdout.write(
                self.style.ERROR('No categories found. Please run load_categories first.')
            )
            return

        # Assign categories to existing articles
        articles_without_category = NewsArticle.objects.filter(category__isnull=True)
        updated_count = 0
        
        for article in articles_without_category:
            # Assign category based on title keywords
            category = self.get_category_by_title(article.title, categories)
            if not category:
                # If no keyword match, assign random category
                category = random.choice(categories)
            
            article.category = category
            article.save()
            updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Assigned "{category.name}" to: {article.title[:50]}...')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} articles with categories!')
        )

    def get_category_by_title(self, title, categories):
        """Assign category based on keywords in title"""
        title_lower = title.lower()
        
        # Define keyword mappings
        keyword_mappings = {
            'politics': ['election', 'government', 'minister', 'president', 'parliament', 'vote', 'policy'],
            'business': ['economic', 'finance', 'company', 'market', 'stock', 'bank', 'trade', 'economy'],
            'technology': ['tech', 'digital', 'software', 'ai', 'artificial intelligence', 'cyber', 'internet'],
            'sports': ['football', 'soccer', 'basketball', 'tennis', 'cricket', 'olympics', 'sport'],
            'health': ['health', 'medical', 'hospital', 'doctor', 'disease', 'medicine', 'covid'],
            'entertainment': ['movie', 'film', 'music', 'celebrity', 'actor', 'singer', 'entertainment'],
            'world': ['international', 'global', 'world', 'country', 'nation', 'diplomatic'],
            'science': ['research', 'study', 'scientist', 'discovery', 'climate', 'environment', 'space']
        }
        
        # Find matching category
        for category in categories:
            category_slug = category.slug
            if category_slug in keyword_mappings:
                keywords = keyword_mappings[category_slug]
                if any(keyword in title_lower for keyword in keywords):
                    return category
        
        return None
