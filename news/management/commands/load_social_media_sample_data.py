from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import SocialMediaPost
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Load sample social media posts for testing'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample social media posts...')
        
        # Sample data
        sample_posts = [
            {
                'title': 'Breaking: Major tech announcement changes everything',
                'content': 'A revolutionary breakthrough in artificial intelligence has been announced by leading tech companies. This development promises to transform how we interact with technology in our daily lives.',
                'platform': 'twitter',
                'author_name': 'TechNews Daily',
                'author_handle': '@technewsdaily',
                'likes': 15420,
                'shares': 3450,
                'comments': 892,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=600&fit=crop'
            },
            {
                'title': 'Global markets show strong recovery signals',
                'content': 'Financial analysts report positive trends across major stock exchanges worldwide. Investors are showing renewed confidence in emerging markets and sustainable energy sectors.',
                'platform': 'linkedin',
                'author_name': 'Financial Times',
                'author_handle': '@ft',
                'likes': 8750,
                'shares': 1890,
                'comments': 456,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop'
            },
            {
                'title': 'Climate change summit reaches historic agreement',
                'content': 'World leaders unite on ambitious climate goals. New policies aim to reduce global carbon emissions by 50% within the next decade. Environmental groups praise the comprehensive approach.',
                'platform': 'facebook',
                'author_name': 'Climate Action Now',
                'author_handle': '@climateactionnow',
                'likes': 23500,
                'shares': 8900,
                'comments': 2100,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e9?w=800&h=600&fit=crop'
            },
            {
                'title': 'Space exploration milestone achieved',
                'content': 'Historic space mission successfully launches new satellite constellation. This achievement marks a significant step forward in global communications and scientific research.',
                'platform': 'instagram',
                'author_name': 'Space Explorer',
                'author_handle': '@spaceexplorer',
                'likes': 45000,
                'shares': 12000,
                'comments': 3400,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=600&fit=crop'
            },
            {
                'title': 'Healthcare innovation improves patient outcomes',
                'content': 'New medical technology demonstrates remarkable success in clinical trials. Patients show 85% improvement rates with the innovative treatment approach.',
                'platform': 'twitter',
                'author_name': 'Medical News Today',
                'author_handle': '@medicalnews',
                'likes': 12300,
                'shares': 4500,
                'comments': 890,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop'
            },
            {
                'title': 'Renewable energy project powers entire city',
                'content': 'A major metropolitan area becomes the first to run entirely on renewable energy. Solar and wind power installations provide sustainable electricity for all residents.',
                'platform': 'linkedin',
                'author_name': 'Green Energy News',
                'author_handle': '@greenenergynews',
                'likes': 9800,
                'shares': 2100,
                'comments': 567,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&h=600&fit=crop'
            },
            {
                'title': 'Educational technology transforms classrooms worldwide',
                'content': 'Revolutionary learning platforms help students achieve better academic results. Teachers report increased engagement and improved learning outcomes across all subjects.',
                'platform': 'facebook',
                'author_name': 'Education Today',
                'author_handle': '@educationtoday',
                'likes': 18700,
                'shares': 6200,
                'comments': 1340,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=600&fit=crop'
            },
            {
                'title': 'Artificial intelligence helps solve global challenges',
                'content': 'AI systems contribute to breakthrough discoveries in medicine, climate science, and sustainable development. Researchers collaborate internationally on pressing issues.',
                'platform': 'twitter',
                'author_name': 'AI Research Hub',
                'author_handle': '@airesearchhub',
                'likes': 21000,
                'shares': 7800,
                'comments': 1900,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1515378960530-7c0da6231fb1?w=800&h=600&fit=crop'
            },
            {
                'title': 'Sustainable fashion industry shows promising growth',
                'content': 'Eco-friendly clothing brands gain popularity among conscious consumers. New materials and production methods reduce environmental impact significantly.',
                'platform': 'instagram',
                'author_name': 'Sustainable Style',
                'author_handle': '@sustainablestyle',
                'likes': 34500,
                'shares': 8900,
                'comments': 2890,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&h=600&fit=crop'
            },
            {
                'title': 'Urban development projects focus on community well-being',
                'content': 'Smart city initiatives prioritize resident quality of life. Green spaces, public transportation, and affordable housing create more livable urban environments.',
                'platform': 'linkedin',
                'author_name': 'Urban Planning Today',
                'author_handle': '@urbanplanningtoday',
                'likes': 7600,
                'shares': 1890,
                'comments': 445,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&h=600&fit=crop'
            }
        ]
        
        # Clear existing posts
        SocialMediaPost.objects.all().delete()
        
        # Create posts
        created_count = 0
        for i, post_data in enumerate(sample_posts):
            # Vary the posting time
            hours_ago = random.randint(1, 72)
            posted_at = timezone.now() - timedelta(hours=hours_ago)
            
            post = SocialMediaPost.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                platform=post_data['platform'],
                author_name=post_data['author_name'],
                author_handle=post_data['author_handle'],
                likes=post_data['likes'],
                shares=post_data['shares'],
                comments=post_data['comments'],
                is_featured=post_data['is_featured'],
                is_active=True,
                posted_at=posted_at,
                image_url=post_data['image_url']
            )
            created_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample social media posts')
        )
