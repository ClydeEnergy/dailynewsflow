from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from news.models import SocialMediaPost
import random


class Command(BaseCommand):
    help = 'Load sample social media posts for testing'

    def handle(self, *args, **options):
        # Clear existing posts
        SocialMediaPost.objects.all().delete()
        
        sample_posts = [
            {
                'title': 'Breaking: Tech Industry Update',
                'content': 'Major developments in artificial intelligence are reshaping the technology landscape. Companies are investing heavily in AI research and development.',
                'platform': 'twitter',
                'author_name': 'TechNews Today',
                'author_handle': '@technewstoday',
                'post_url': 'https://twitter.com/technewstoday/status/123456789',
                'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=500&h=300&fit=crop',
                'likes': 1250,
                'shares': 340,
                'comments': 89,
                'is_featured': True,
            },
            {
                'title': 'Global Market Trends',
                'content': 'Stock markets around the world are showing mixed signals as investors react to the latest economic indicators and policy changes.',
                'platform': 'linkedin',
                'author_name': 'Financial Times',
                'author_handle': '@ft',
                'post_url': 'https://linkedin.com/posts/financial-times',
                'image_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500&h=300&fit=crop',
                'likes': 890,
                'shares': 156,
                'comments': 67,
                'is_featured': True,
            },
            {
                'title': 'Climate Change Initiative',
                'content': 'New environmental policies are being implemented globally to combat climate change and promote sustainable development.',
                'platform': 'facebook',
                'author_name': 'Green Planet News',
                'author_handle': '@greenplanetnews',
                'post_url': 'https://facebook.com/greenplanetnews/posts/123',
                'image_url': 'https://images.unsplash.com/photo-1569163139071-de7d3b6f31d0?w=500&h=300&fit=crop',
                'likes': 2100,
                'shares': 567,
                'comments': 234,
                'is_featured': False,
            },
            {
                'title': 'Sports Championship Updates',
                'content': 'The championship finals are approaching with intense competition between top teams. Fans are eagerly awaiting the final matches.',
                'platform': 'instagram',
                'author_name': 'Sports Central',
                'author_handle': '@sportscentral',
                'post_url': 'https://instagram.com/p/sportscentral123',
                'image_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&h=300&fit=crop',
                'likes': 3400,
                'shares': 890,
                'comments': 456,
                'is_featured': False,
            },
            {
                'title': 'Healthcare Innovation',
                'content': 'Revolutionary medical treatments are being developed using cutting-edge technology and research methodologies.',
                'platform': 'twitter',
                'author_name': 'Medical Today',
                'author_handle': '@medicaltoday',
                'post_url': 'https://twitter.com/medicaltoday/status/987654321',
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=500&h=300&fit=crop',
                'likes': 756,
                'shares': 123,
                'comments': 45,
                'is_featured': False,
            },
            {
                'title': 'Education Technology Trends',
                'content': 'Digital learning platforms are transforming education worldwide, making quality education accessible to more students.',
                'platform': 'linkedin',
                'author_name': 'EduTech Weekly',
                'author_handle': '@edutechweekly',
                'post_url': 'https://linkedin.com/posts/edutech-weekly',
                'image_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500&h=300&fit=crop',
                'likes': 445,
                'shares': 89,
                'comments': 23,
                'is_featured': True,
            },
            {
                'title': 'Travel Industry Recovery',
                'content': 'The travel industry is showing signs of recovery with new destinations opening up and tourism numbers increasing.',
                'platform': 'instagram',
                'author_name': 'Travel Explorer',
                'author_handle': '@travelexplorer',
                'post_url': 'https://instagram.com/p/travelexplorer456',
                'image_url': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=500&h=300&fit=crop',
                'likes': 1890,
                'shares': 345,
                'comments': 178,
                'is_featured': False,
            },
            {
                'title': 'Space Exploration Update',
                'content': 'NASA announces new discoveries from the latest space mission, providing insights into deep space exploration.',
                'platform': 'twitter',
                'author_name': 'Space News Network',
                'author_handle': '@spacenewsnet',
                'post_url': 'https://twitter.com/spacenewsnet/status/456789123',
                'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=500&h=300&fit=crop',
                'likes': 2750,
                'shares': 678,
                'comments': 289,
                'is_featured': True,
            },
        ]
        
        created_count = 0
        
        for i, post_data in enumerate(sample_posts):
            # Calculate posted_at time (spread over the last 7 days)
            days_ago = random.randint(0, 6)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            posted_at = timezone.now() - timedelta(
                days=days_ago, 
                hours=hours_ago, 
                minutes=minutes_ago
            )
            
            post = SocialMediaPost.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                platform=post_data['platform'],
                author_name=post_data['author_name'],
                author_handle=post_data['author_handle'],
                post_url=post_data['post_url'],
                image_url=post_data['image_url'],
                likes=post_data['likes'],
                shares=post_data['shares'],
                comments=post_data['comments'],
                is_featured=post_data['is_featured'],
                is_active=True,
                posted_at=posted_at,
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created post: {post.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample social media posts!')
        )
