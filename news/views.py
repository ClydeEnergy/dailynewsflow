from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import NewsArticle, Country, NewsProvider, MarketTicker, Commodity, Cryptocurrency, SocialMediaPost, Category, ExchangeRate
import json


class MarketDetailView(DetailView):
    """Detail view for market tickers"""
    model = MarketTicker
    template_name = 'news/market_detail.html'
    context_object_name = 'ticker'

    def get_queryset(self):
        return MarketTicker.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.get_object()
        
        # Get related news articles (search by ticker symbol in title or description)
        context['related_articles'] = NewsArticle.objects.filter(
            Q(title__icontains=ticker.symbol) | Q(description__icontains=ticker.symbol),
            is_active=True
        ).order_by('-date_posted')[:5]
        
        # Get other active tickers for sidebar
        context['other_tickers'] = MarketTicker.objects.filter(
            is_active=True
        ).exclude(id=ticker.id).order_by('symbol')[:10]
        
        return context


class MarketsView(ListView):
    """Markets page view displaying all financial market data"""
    model = MarketTicker
    template_name = 'news/markets.html'
    context_object_name = 'market_tickers'

    def get_queryset(self):
        return MarketTicker.objects.filter(is_active=True).order_by('symbol')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get exchange rates
        context['exchange_rates'] = ExchangeRate.objects.filter(
            is_active=True
        ).order_by('currency_pair')
        
        # Get commodities
        context['commodities'] = Commodity.objects.filter(
            is_active=True
        ).order_by('name')
        
        # Get cryptocurrencies
        context['cryptocurrencies'] = Cryptocurrency.objects.filter(
            is_active=True
        ).order_by('name')
        
        return context


class HomeView(ListView):
    """Home page view displaying news articles with professional dashboard"""
    model = NewsArticle
    template_name = 'news/home.html'
    context_object_name = 'recent_articles'
    paginate_by = 12

    def get_queryset(self):
        queryset = NewsArticle.objects.filter(is_active=True).order_by('-date_posted')
        
        # Apply filters
        from_date = self.request.GET.get('from_date')
        country = self.request.GET.get('country')
        category = self.request.GET.get('category')
        
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date_posted__gte=from_date)
            except ValueError:
                pass
                
        if country:
            queryset = queryset.filter(country__code=country)
            
        if category:
            if category == 'breaking':
                # For breaking news, show recent articles from the last 24 hours
                yesterday = timezone.now() - timezone.timedelta(days=1)
                queryset = queryset.filter(date_posted__gte=yesterday)
            else:
                # Filter by category slug
                queryset = queryset.filter(category__slug=category)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get latest articles (remove breaking news section, just show latest)
        recent_articles = NewsArticle.objects.filter(is_active=True).order_by('-date_posted')[:12]
        
        # Apply same filters to get filtered recent articles
        from_date = self.request.GET.get('from_date')
        country_code = self.request.GET.get('country')
        category = self.request.GET.get('category')
        
        if from_date or country_code or category:
            recent_articles = self.get_queryset()[:12]
        
        # Get categories for navigation and filters
        categories = Category.objects.filter(is_active=True).order_by('name')
        
        # Get market data
        market_tickers = MarketTicker.objects.filter(is_active=True).order_by('symbol')[:10]
        commodities = Commodity.objects.filter(is_active=True).order_by('name')[:5]
        cryptocurrencies = Cryptocurrency.objects.filter(is_active=True).order_by('name')[:5]
        exchange_rates = ExchangeRate.objects.filter(is_active=True).order_by('base_currency', 'quote_currency')[:8]
        
        # Get countries with article counts
        countries = Country.objects.filter(is_active=True).annotate(
            article_count=Count('articles', filter=Q(articles__is_active=True))
        ).order_by('name')
        
        # Get top countries by article count
        top_countries = countries.filter(article_count__gt=0).order_by('-article_count')[:10]
        
        # Get social media posts for bottom section
        social_posts = SocialMediaPost.objects.filter(is_active=True).order_by('-created_at')[:6]
        
        # Get statistics
        total_articles = NewsArticle.objects.filter(is_active=True).count()
        total_countries = countries.count()
        total_providers = NewsProvider.objects.filter(is_active=True).count()
        
        # Date helpers
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        context.update({
            'recent_articles': recent_articles,
            'categories': categories,
            'market_tickers': market_tickers,
            'commodities': commodities,
            'cryptocurrencies': cryptocurrencies,
            'exchange_rates': exchange_rates,
            'countries': countries,
            'top_countries': top_countries,
            'social_posts': social_posts,
            'total_articles': total_articles,
            'total_countries': total_countries,
            'total_providers': total_providers,
            'today': today,
            'week_ago': week_ago,
            'month_ago': month_ago,
        })
        
        return context


class ArticleDetailView(DetailView):
    """Detail view for individual articles"""
    model = NewsArticle
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return NewsArticle.objects.filter(is_active=True).select_related(
            'country', 'news_provider'
        )

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        # Increment view count
        article.increment_views()
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Get related articles (same country or provider)
        context['related_articles'] = NewsArticle.objects.filter(
            Q(country=article.country) | Q(news_provider=article.news_provider),
            is_active=True
        ).exclude(id=article.id).select_related('country', 'news_provider')[:4]
        
        return context


class CountryView(ListView):
    """View for articles by country"""
    model = NewsArticle
    template_name = 'news/country.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        self.country = get_object_or_404(Country, code=self.kwargs['code'], is_active=True)
        return NewsArticle.objects.filter(
            country=self.country, is_active=True
        ).select_related('country', 'news_provider').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = self.country
        context['countries'] = Country.objects.filter(
            is_active=True, articles__is_active=True
        ).annotate(article_count=Count('articles')).order_by('-article_count')[:10]
        return context


class ProviderView(ListView):
    """View for articles by news provider"""
    model = NewsArticle
    template_name = 'news/provider.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        self.provider = get_object_or_404(NewsProvider, id=self.kwargs['pk'], is_active=True)
        return NewsArticle.objects.filter(
            news_provider=self.provider, is_active=True
        ).select_related('country', 'news_provider').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provider'] = self.provider
        context['providers'] = NewsProvider.objects.filter(
            is_active=True, articles__is_active=True
        ).annotate(article_count=Count('articles')).order_by('-article_count')[:10]
        return context


class SearchView(ListView):
    """Search view for articles"""
    model = NewsArticle
    template_name = 'news/search.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return NewsArticle.objects.none()

        return NewsArticle.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query),
            is_active=True
        ).select_related('country', 'news_provider').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['countries'] = Country.objects.filter(
            is_active=True, articles__is_active=True
        ).annotate(article_count=Count('articles')).order_by('-article_count')
        return context


class CategoryView(ListView):
    """View for displaying articles by category"""
    model = NewsArticle
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return NewsArticle.objects.filter(
            category=self.category,
            is_active=True
        ).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['page_title'] = f"{self.category.name} News"
        context['categories'] = Category.objects.filter(is_active=True).exclude(id=self.category.id).order_by('name')
        context['recent_articles'] = NewsArticle.objects.filter(is_active=True).order_by('-date_posted')[:10]
        return context


class AllNewsView(ListView):
    """View for displaying all news articles with filtering and pagination"""
    model = NewsArticle
    template_name = 'news/all_news.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        queryset = NewsArticle.objects.filter(is_active=True).select_related(
            'country', 'news_provider', 'category'
        ).order_by('-date_posted')
        
        # Filter by search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by country
        country_code = self.request.GET.get('country')
        if country_code:
            queryset = queryset.filter(country__code=country_code)
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by date range
        from_date = self.request.GET.get('from_date')
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date_posted__date__gte=from_date)
            except ValueError:
                pass
        
        to_date = self.request.GET.get('to_date')
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date_posted__date__lte=to_date)
            except ValueError:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['countries'] = Country.objects.filter(is_active=True).annotate(
            article_count=Count('articles', filter=Q(articles__is_active=True))
        ).filter(article_count__gt=0).order_by('name')
        
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            article_count=Count('articles', filter=Q(articles__is_active=True))
        ).filter(article_count__gt=0).order_by('name')
        
        # Add current filter values
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'country': self.request.GET.get('country', ''),
            'category': self.request.GET.get('category', ''),
            'from_date': self.request.GET.get('from_date', ''),
            'to_date': self.request.GET.get('to_date', ''),
        }
        
        context['total_results'] = self.get_queryset().count()
        
        return context


class SocialMediaView(ListView):
    """View for displaying social media posts"""
    model = SocialMediaPost
    template_name = 'news/social_media.html'
    context_object_name = 'posts'
    paginate_by = 16

    def get_queryset(self):
        queryset = SocialMediaPost.objects.filter(is_active=True).order_by('-created_at')
        
        # Filter by platform
        platform = self.request.GET.get('platform')
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Filter by search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) |
                Q(author_name__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add platform choices for filtering
        context['platforms'] = SocialMediaPost.PLATFORM_CHOICES
        
        # Add current filter values
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'platform': self.request.GET.get('platform', ''),
        }
        
        context['total_results'] = self.get_queryset().count()
        
        # Add platform statistics
        context['platform_stats'] = []
        for platform_code, platform_name in SocialMediaPost.PLATFORM_CHOICES:
            count = SocialMediaPost.objects.filter(
                platform=platform_code, 
                is_active=True
            ).count()
            if count > 0:
                context['platform_stats'].append({
                    'code': platform_code,
                    'name': platform_name,
                    'count': count
                })
        
        # Add platform statistics
        context['platform_stats'] = []
        for platform_code, platform_name in SocialMediaPost.PLATFORM_CHOICES:
            count = SocialMediaPost.objects.filter(
                platform=platform_code, 
                is_active=True
            ).count()
            if count > 0:
                context['platform_stats'].append({
                    'code': platform_code,
                    'name': platform_name,
                    'count': count
                })
        
        return context


class AllSocialPostsView(ListView):
    """Public view for displaying all social media posts with filtering"""
    model = SocialMediaPost
    template_name = 'news/all_social_posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = SocialMediaPost.objects.filter(is_active=True).order_by('-created_at')
        
        # Filter by platform
        platform = self.request.GET.get('platform')
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Filter by search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) |
                Q(author_name__icontains=search_query)
            )
        
        # Filter by date range
        from_date = self.request.GET.get('from_date')
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__gte=from_date)
            except ValueError:
                pass
        
        to_date = self.request.GET.get('to_date')
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__lte=to_date)
            except ValueError:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add platform choices for filtering
        context['platforms'] = SocialMediaPost.PLATFORM_CHOICES
        
        # Add current filter values
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'platform': self.request.GET.get('platform', ''),
            'from_date': self.request.GET.get('from_date', ''),
            'to_date': self.request.GET.get('to_date', ''),
        }
        
        context['total_results'] = self.get_queryset().count()
        
        # Add platform statistics
        context['platform_stats'] = []
        for platform_code, platform_name in SocialMediaPost.PLATFORM_CHOICES:
            count = SocialMediaPost.objects.filter(
                platform=platform_code, 
                is_active=True
            ).count()
            if count > 0:
                context['platform_stats'].append({
                    'code': platform_code,
                    'name': platform_name,
                    'count': count
                })
        
        # Add recent posts for sidebar
        context['recent_posts'] = SocialMediaPost.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5]
        
        return context


@require_http_methods(["GET"])
def filter_articles(request):
    """AJAX endpoint for filtering articles"""
    country_id = request.GET.get('country')
    provider_id = request.GET.get('provider')
    search_query = request.GET.get('search', '')

    articles = NewsArticle.objects.filter(is_active=True)

    if country_id:
        articles = articles.filter(country_id=country_id)
    
    if provider_id:
        articles = articles.filter(news_provider_id=provider_id)
    
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    articles = articles.select_related('country', 'news_provider').order_by('-date_posted')[:20]

    articles_data = []
    for article in articles:
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'description': article.description[:150] + '...' if len(article.description) > 150 else article.description,
            'image': article.image,
            'link': article.link,
            'date_posted': article.date_posted.strftime('%Y-%m-%d %H:%M'),
            'country': {
                'name': article.country.name,
                'code': article.country.code,
            },
            'provider': {
                'name': article.news_provider.name,
                'website': article.news_provider.website,
            },
            'views': article.views,
        })

    return JsonResponse({
        'articles': articles_data,
        'total_count': len(articles_data)
    })


@require_http_methods(["GET"])
def get_article_stats(request):
    """Get statistics for the dashboard"""
    stats = {
        'total_articles': NewsArticle.objects.filter(is_active=True).count(),
        'total_countries': Country.objects.filter(is_active=True).count(),
        'total_providers': NewsProvider.objects.filter(is_active=True).count(),
        'articles_today': NewsArticle.objects.filter(
            is_active=True, 
            created_at__date=timezone.now().date()
        ).count(),
    }

    # Top countries by article count
    country_stats = Country.objects.filter(is_active=True).annotate(
        article_count=Count('articles', filter=Q(articles__is_active=True))
    ).order_by('-article_count')[:5]

    # Top providers by article count
    provider_stats = NewsProvider.objects.filter(is_active=True).annotate(
        article_count=Count('articles', filter=Q(articles__is_active=True))
    ).order_by('-article_count')[:5]

    stats['top_countries'] = [
        {'name': country.name, 'count': country.article_count}
        for country in country_stats
    ]
    
    stats['top_providers'] = [
        {'name': provider.name, 'count': provider.article_count}
        for provider in provider_stats
    ]

    return JsonResponse(stats)


def about_view(request):
    """About page view"""
    return render(request, 'news/about.html')


def contact_view(request):
    """Contact page view"""
    return render(request, 'news/contact.html')