from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import NewsArticle, Country, NewsProvider, MarketTicker, Commodity, Cryptocurrency, SocialMediaPost, ExchangeRate
from .forms import (NewsArticleForm, AdminLoginForm, AdminUserForm, CountryForm, NewsProviderForm,
                   MarketTickerForm, CommodityForm, CryptocurrencyForm, SocialMediaPostForm, ExchangeRateForm)


def is_admin_user(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_superuser(user):
    """Check if user is superuser"""
    return user.is_authenticated and user.is_superuser


@csrf_protect
def admin_login(request):
    """Custom admin login view"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('news:admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and (user.is_staff or user.is_superuser):
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'news:admin_dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = AdminLoginForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', '')
    }
    return render(request, 'admin/login.html', context)


@login_required
def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('news:admin_login')


@user_passes_test(is_superuser, login_url='news:admin_login')
def admin_users(request):
    """Manage admin users"""
    search_query = request.GET.get('search', '')
    
    users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    users = users.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/users.html', context)


@user_passes_test(is_superuser, login_url='/admin/login/')
def admin_add_user(request):
    """Add new admin user"""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" has been created successfully.')
            return redirect('news:admin_users')
    else:
        form = AdminUserForm()
    
    context = {
        'form': form,
        'title': 'Add Admin User',
        'submit_text': 'Create User'
    }
    
    return render(request, 'admin/user_form.html', context)


@user_passes_test(is_superuser, login_url='/admin/login/')
def admin_edit_user(request, pk):
    """Edit admin user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user, is_edit=True)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" has been updated successfully.')
            return redirect('news:admin_users')
    else:
        form = AdminUserForm(instance=user, is_edit=True)
    
    context = {
        'form': form,
        'user_obj': user,
        'title': 'Edit Admin User',
        'submit_text': 'Update User'
    }
    
    return render(request, 'admin/user_form.html', context)


@user_passes_test(is_superuser, login_url='/admin/login/')
def admin_delete_user(request, pk):
    """Delete admin user"""
    user = get_object_or_404(User, pk=pk)
    
    # Prevent deletion of the current user
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('news:admin_users')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been deleted successfully.')
        return redirect('news:admin_users')
    
    context = {
        'user_obj': user,
        'title': 'Delete Admin User'
    }
    
    return render(request, 'admin/user_delete.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    # Get statistics
    total_articles = NewsArticle.objects.count()
    active_articles = NewsArticle.objects.filter(is_active=True).count()
    total_countries = Country.objects.count()
    total_providers = NewsProvider.objects.count()
    
    # Recent articles
    recent_articles = NewsArticle.objects.select_related('country', 'news_provider').order_by('-created_at')[:10]
    
    # Top countries by article count
    top_countries = Country.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:5]
    
    # Top providers by article count
    top_providers = NewsProvider.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:5]
    
    # Articles created today
    today = timezone.now().date()
    articles_today = NewsArticle.objects.filter(created_at__date=today).count()
    
    # Market data statistics
    total_market_tickers = MarketTicker.objects.count()
    total_commodities = Commodity.objects.count()
    total_cryptocurrencies = Cryptocurrency.objects.count()
    total_exchange_rates = ExchangeRate.objects.count()
    active_exchange_rates = ExchangeRate.objects.filter(is_active=True).count()
    
    # Social media posts statistics
    total_social_posts = SocialMediaPost.objects.count()
    active_social_posts = SocialMediaPost.objects.filter(is_active=True).count()
    featured_social_posts = SocialMediaPost.objects.filter(is_featured=True).count()
    posts_today = SocialMediaPost.objects.filter(created_at__date=today).count()
    
    # Recent social media posts
    recent_social_posts = SocialMediaPost.objects.order_by('-created_at')[:5]
    
    # Recent exchange rates
    recent_exchange_rates = ExchangeRate.objects.filter(is_active=True).order_by('-last_updated')[:8]
    
    context = {
        'total_articles': total_articles,
        'active_articles': active_articles,
        'total_countries': total_countries,
        'total_providers': total_providers,
        'recent_articles': recent_articles,
        'top_countries': top_countries,
        'top_providers': top_providers,
        'articles_today': articles_today,
        'total_market_tickers': total_market_tickers,
        'total_commodities': total_commodities,
        'total_cryptocurrencies': total_cryptocurrencies,
        'total_exchange_rates': total_exchange_rates,
        'active_exchange_rates': active_exchange_rates,
        'total_social_posts': total_social_posts,
        'active_social_posts': active_social_posts,
        'featured_social_posts': featured_social_posts,
        'posts_today': posts_today,
        'recent_social_posts': recent_social_posts,
        'recent_exchange_rates': recent_exchange_rates,
    }
    
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_articles(request):
    """Manage news articles"""
    search_query = request.GET.get('search', '')
    country_filter = request.GET.get('country', '')
    provider_filter = request.GET.get('provider', '')
    status_filter = request.GET.get('status', '')
    
    articles = NewsArticle.objects.select_related('country', 'news_provider')
    
    # Apply filters
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if country_filter:
        articles = articles.filter(country_id=country_filter)
    
    if provider_filter:
        articles = articles.filter(news_provider_id=provider_filter)
    
    if status_filter:
        is_active = status_filter == 'active'
        articles = articles.filter(is_active=is_active)
    
    articles = articles.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(articles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    countries = Country.objects.filter(is_active=True).order_by('name')
    providers = NewsProvider.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'countries': countries,
        'providers': providers,
        'country_filter': country_filter,
        'provider_filter': provider_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/articles.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_article(request):
    """Add new news article"""
    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" has been created successfully.')
            return redirect('news:admin_articles')
    else:
        form = NewsArticleForm()
    
    context = {
        'form': form,
        'title': 'Add News Article',
        'submit_text': 'Create Article'
    }
    
    return render(request, 'admin/article_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_article(request, pk):
    """Edit news article"""
    article = get_object_or_404(NewsArticle, pk=pk)
    
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" has been updated successfully.')
            return redirect('news:admin_articles')
    else:
        form = NewsArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
        'title': 'Edit News Article',
        'submit_text': 'Update Article'
    }
    
    return render(request, 'admin/article_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_article(request, pk):
    """Delete news article"""
    article = get_object_or_404(NewsArticle, pk=pk)
    
    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'Article "{title}" has been deleted successfully.')
        return redirect('news:admin_articles')
    
    context = {
        'article': article,
        'title': 'Delete News Article'
    }
    
    return render(request, 'admin/article_delete.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_countries(request):
    """Manage countries"""
    search_query = request.GET.get('search', '')
    
    countries = Country.objects.annotate(
        article_count=Count('articles')
    )
    
    if search_query:
        countries = countries.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query)
        )
    
    countries = countries.order_by('name')
    
    # Pagination
    paginator = Paginator(countries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/countries.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_country(request):
    """Add new country"""
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            messages.success(request, f'Country "{country.name}" added successfully!')
            return redirect('news:admin_countries')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CountryForm()
    
    context = {
        'form': form,
        'action': 'Add',
        'title': 'Add New Country'
    }
    return render(request, 'admin/country_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_country(request, pk):
    """Edit country"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            country = form.save()
            messages.success(request, f'Country "{country.name}" updated successfully!')
            return redirect('news:admin_countries')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CountryForm(instance=country)
    
    context = {
        'form': form,
        'country': country,
        'action': 'Edit',
        'title': f'Edit Country - {country.name}'
    }
    return render(request, 'admin/country_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_providers(request):
    """Manage news providers"""
    search_query = request.GET.get('search', '')
    
    providers = NewsProvider.objects.select_related('country').annotate(
        article_count=Count('articles')
    )
    
    if search_query:
        providers = providers.filter(
            Q(name__icontains=search_query) | 
            Q(website__icontains=search_query) |
            Q(country__name__icontains=search_query)
        )
    
    providers = providers.order_by('name')
    
    # Pagination
    paginator = Paginator(providers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/providers.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_provider(request):
    """Add new news provider"""
    if request.method == 'POST':
        form = NewsProviderForm(request.POST)
        if form.is_valid():
            provider = form.save()
            messages.success(request, f'News provider "{provider.name}" added successfully!')
            return redirect('news:admin_providers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsProviderForm()
    
    context = {
        'form': form,
        'action': 'Add',
        'title': 'Add New News Provider'
    }
    return render(request, 'admin/provider_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_provider(request, pk):
    """Edit news provider"""
    provider = get_object_or_404(NewsProvider, pk=pk)
    
    if request.method == 'POST':
        form = NewsProviderForm(request.POST, instance=provider)
        if form.is_valid():
            provider = form.save()
            messages.success(request, f'News provider "{provider.name}" updated successfully!')
            return redirect('news:admin_providers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsProviderForm(instance=provider)
    
    context = {
        'form': form,
        'provider': provider,
        'action': 'Edit',
        'title': f'Edit News Provider - {provider.name}'
    }
    return render(request, 'admin/provider_form.html', context)


@require_http_methods(["POST"])
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_toggle_article_status(request, pk):
    """Toggle article active status"""
    article = get_object_or_404(NewsArticle, pk=pk)
    article.is_active = not article.is_active
    article.save(update_fields=['is_active'])
    
    status = "activated" if article.is_active else "deactivated"
    messages.success(request, f'Article "{article.title}" has been {status}.')
    
    return JsonResponse({'success': True, 'is_active': article.is_active})


# Market Ticker Views
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_market_tickers(request):
    """Manage market tickers"""
    search_query = request.GET.get('search', '')
    
    tickers = MarketTicker.objects.all()
    
    if search_query:
        tickers = tickers.filter(
            Q(symbol__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(exchange__icontains=search_query)
        )
    
    tickers = tickers.order_by('symbol')
    
    # Pagination
    paginator = Paginator(tickers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/market_tickers.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_market_ticker(request):
    """Add new market ticker"""
    if request.method == 'POST':
        form = MarketTickerForm(request.POST)
        if form.is_valid():
            ticker = form.save()
            messages.success(request, f'Market ticker "{ticker.symbol}" has been added successfully.')
            return redirect('news:admin_market_tickers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MarketTickerForm()
    
    context = {
        'form': form,
        'title': 'Add Market Ticker',
        'submit_text': 'Add Ticker'
    }
    return render(request, 'admin/market_ticker_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_market_ticker(request, pk):
    """Edit market ticker"""
    ticker = get_object_or_404(MarketTicker, pk=pk)
    
    if request.method == 'POST':
        form = MarketTickerForm(request.POST, instance=ticker)
        if form.is_valid():
            form.save()
            messages.success(request, f'Market ticker "{ticker.symbol}" has been updated successfully.')
            return redirect('news:admin_market_tickers')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MarketTickerForm(instance=ticker)
    
    context = {
        'form': form,
        'ticker': ticker,
        'title': f'Edit Market Ticker - {ticker.symbol}',
        'submit_text': 'Update Ticker'
    }
    return render(request, 'admin/market_ticker_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_market_ticker(request, pk):
    """Delete market ticker"""
    ticker = get_object_or_404(MarketTicker, pk=pk)
    
    if request.method == 'POST':
        ticker_symbol = ticker.symbol
        ticker.delete()
        messages.success(request, f'Market ticker "{ticker_symbol}" has been deleted successfully.')
        return redirect('news:admin_market_tickers')
    
    context = {
        'object': ticker,
        'object_type': 'Market Ticker',
        'object_name': ticker.symbol
    }
    return render(request, 'admin/confirm_delete.html', context)


# Commodity Views
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_commodities(request):
    """Manage commodities"""
    search_query = request.GET.get('search', '')
    
    commodities = Commodity.objects.all()
    
    if search_query:
        commodities = commodities.filter(
            Q(name__icontains=search_query) |
            Q(symbol__icontains=search_query) |
            Q(unit__icontains=search_query)
        )
    
    commodities = commodities.order_by('name')
    
    # Pagination
    paginator = Paginator(commodities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/commodities.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_commodity(request):
    """Add new commodity"""
    if request.method == 'POST':
        form = CommodityForm(request.POST)
        if form.is_valid():
            commodity = form.save()
            messages.success(request, f'Commodity "{commodity.name}" has been added successfully.')
            return redirect('news:admin_commodities')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommodityForm()
    
    context = {
        'form': form,
        'title': 'Add Commodity',
        'submit_text': 'Add Commodity'
    }
    return render(request, 'admin/commodity_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_commodity(request, pk):
    """Edit commodity"""
    commodity = get_object_or_404(Commodity, pk=pk)
    
    if request.method == 'POST':
        form = CommodityForm(request.POST, instance=commodity)
        if form.is_valid():
            form.save()
            messages.success(request, f'Commodity "{commodity.name}" has been updated successfully.')
            return redirect('news:admin_commodities')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommodityForm(instance=commodity)
    
    context = {
        'form': form,
        'commodity': commodity,
        'title': f'Edit Commodity - {commodity.name}',
        'submit_text': 'Update Commodity'
    }
    return render(request, 'admin/commodity_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_commodity(request, pk):
    """Delete commodity"""
    commodity = get_object_or_404(Commodity, pk=pk)
    
    if request.method == 'POST':
        commodity_name = commodity.name
        commodity.delete()
        messages.success(request, f'Commodity "{commodity_name}" has been deleted successfully.')
        return redirect('news:admin_commodities')
    
    context = {
        'object': commodity,
        'object_type': 'Commodity',
        'object_name': commodity.name
    }
    return render(request, 'admin/confirm_delete.html', context)


# Cryptocurrency Views
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_cryptocurrencies(request):
    """Manage cryptocurrencies"""
    search_query = request.GET.get('search', '')
    
    cryptocurrencies = Cryptocurrency.objects.all()
    
    if search_query:
        cryptocurrencies = cryptocurrencies.filter(
            Q(name__icontains=search_query) |
            Q(symbol__icontains=search_query)
        )
    
    cryptocurrencies = cryptocurrencies.order_by('-market_cap')
    
    # Pagination
    paginator = Paginator(cryptocurrencies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'admin/cryptocurrencies.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_cryptocurrency(request):
    """Add new cryptocurrency"""
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST)
        if form.is_valid():
            crypto = form.save()
            messages.success(request, f'Cryptocurrency "{crypto.name}" has been added successfully.')
            return redirect('news:admin_cryptocurrencies')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CryptocurrencyForm()
    
    context = {
        'form': form,
        'title': 'Add Cryptocurrency',
        'submit_text': 'Add Cryptocurrency'
    }
    return render(request, 'admin/cryptocurrency_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_cryptocurrency(request, pk):
    """Edit cryptocurrency"""
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        form = CryptocurrencyForm(request.POST, instance=crypto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cryptocurrency "{crypto.name}" has been updated successfully.')
            return redirect('news:admin_cryptocurrencies')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CryptocurrencyForm(instance=crypto)
    
    context = {
        'form': form,
        'crypto': crypto,
        'title': f'Edit Cryptocurrency - {crypto.name}',
        'submit_text': 'Update Cryptocurrency'
    }
    return render(request, 'admin/cryptocurrency_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_cryptocurrency(request, pk):
    """Delete cryptocurrency"""
    crypto = get_object_or_404(Cryptocurrency, pk=pk)
    
    if request.method == 'POST':
        crypto_name = crypto.name
        crypto.delete()
        messages.success(request, f'Cryptocurrency "{crypto_name}" has been deleted successfully.')
        return redirect('news:admin_cryptocurrencies')
    
    context = {
        'object': crypto,
        'object_type': 'Cryptocurrency',
        'object_name': crypto.name
    }
    return render(request, 'admin/confirm_delete.html', context)


# Social Media Posts Views
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_social_posts(request):
    """List all social media posts"""
    posts = SocialMediaPost.objects.all().order_by('-posted_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author_name__icontains=search_query) |
            Q(platform__icontains=search_query)
        )
    
    # Filter by platform
    platform_filter = request.GET.get('platform', '')
    if platform_filter:
        posts = posts.filter(platform=platform_filter)
    
    # Filter by active status
    active_filter = request.GET.get('active', '')
    if active_filter:
        is_active = active_filter.lower() == 'true'
        posts = posts.filter(is_active=is_active)
    
    # Pagination
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get platform choices for filter
    platform_choices = SocialMediaPost.PLATFORM_CHOICES
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'search_query': search_query,
        'platform_filter': platform_filter,
        'active_filter': active_filter,
        'platform_choices': platform_choices,
        'total_posts': posts.count(),
        'active_posts': posts.filter(is_active=True).count(),
    }
    return render(request, 'admin/social_posts.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_social_post(request):
    """Add new social media post"""
    if request.method == 'POST':
        form = SocialMediaPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Social media post "{post.title}" has been created successfully.')
            return redirect('news:admin_social_posts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SocialMediaPostForm()
    
    context = {
        'form': form,
        'title': 'Add New Social Media Post',
        'action': 'Add'
    }
    return render(request, 'admin/social_post_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_social_post(request, pk):
    """Edit social media post"""
    post = get_object_or_404(SocialMediaPost, pk=pk)
    
    if request.method == 'POST':
        form = SocialMediaPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Social media post "{post.title}" has been updated successfully.')
            return redirect('news:admin_social_posts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SocialMediaPostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': f'Edit Social Media Post - {post.title}',
        'action': 'Edit'
    }
    return render(request, 'admin/social_post_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_social_post(request, pk):
    """Delete social media post"""
    post = get_object_or_404(SocialMediaPost, pk=pk)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Social media post "{post_title}" has been deleted successfully.')
        return redirect('news:admin_social_posts')
    
    context = {
        'object': post,
        'object_type': 'Social Media Post',
        'object_name': post.title
    }
    return render(request, 'admin/confirm_delete.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
@require_http_methods(["POST"])
def admin_toggle_social_post_status(request, pk):
    """Toggle social media post active status via AJAX"""
    post = get_object_or_404(SocialMediaPost, pk=pk)
    post.is_active = not post.is_active
    post.save()
    
    return JsonResponse({
        'success': True,
        'is_active': post.is_active,
        'message': f'Post status updated to {"Active" if post.is_active else "Inactive"}'
    })


@user_passes_test(is_admin_user, login_url='news:admin_login')
@require_http_methods(["POST"])
def admin_toggle_social_post_featured(request, pk):
    """Toggle social media post featured status via AJAX"""
    post = get_object_or_404(SocialMediaPost, pk=pk)
    post.is_featured = not post.is_featured
    post.save()
    
    return JsonResponse({
        'success': True,
        'is_featured': post.is_featured,
        'message': f'Post {"featured" if post.is_featured else "unfeatured"} successfully'
    })


# Exchange Rate Views
@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_exchange_rates(request):
    """Manage exchange rates"""
    search_query = request.GET.get('search', '')
    market_filter = request.GET.get('market', '')
    
    exchange_rates = ExchangeRate.objects.all()
    
    if search_query:
        exchange_rates = exchange_rates.filter(
            Q(currency_pair__icontains=search_query) |
            Q(base_currency__icontains=search_query) |
            Q(quote_currency__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if market_filter:
        exchange_rates = exchange_rates.filter(market=market_filter)
    
    exchange_rates = exchange_rates.order_by('currency_pair')
    
    # Pagination
    paginator = Paginator(exchange_rates, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get statistics
    total_exchange_rates = ExchangeRate.objects.count()
    active_exchange_rates = ExchangeRate.objects.filter(is_active=True).count()
    forex_rates = ExchangeRate.objects.filter(market='forex').count()
    crypto_rates = ExchangeRate.objects.filter(market='crypto').count()
    
    # Get market choices for filter
    market_choices = ExchangeRate.MARKET_CHOICES
    
    context = {
        'exchange_rates': page_obj,  # Change from page_obj to exchange_rates
        'total_exchange_rates': total_exchange_rates,
        'active_exchange_rates': active_exchange_rates,
        'forex_rates': forex_rates,
        'crypto_rates': crypto_rates,
        'search_query': search_query,
        'market_filter': market_filter,
        'market_choices': market_choices,
    }
    
    return render(request, 'admin/exchange_rates.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_add_exchange_rate(request):
    """Add new exchange rate"""
    if request.method == 'POST':
        form = ExchangeRateForm(request.POST)
        if form.is_valid():
            exchange_rate = form.save()
            messages.success(request, f'Exchange rate "{exchange_rate.currency_pair}" has been added successfully.')
            return redirect('news:admin_exchange_rates')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExchangeRateForm()
    
    context = {
        'form': form,
        'title': 'Add Exchange Rate',
        'submit_text': 'Add Exchange Rate'
    }
    return render(request, 'admin/exchange_rate_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_edit_exchange_rate(request, pk):
    """Edit exchange rate"""
    exchange_rate = get_object_or_404(ExchangeRate, pk=pk)
    
    if request.method == 'POST':
        form = ExchangeRateForm(request.POST, instance=exchange_rate)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exchange rate "{exchange_rate.currency_pair}" has been updated successfully.')
            return redirect('news:admin_exchange_rates')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExchangeRateForm(instance=exchange_rate)
    
    context = {
        'form': form,
        'exchange_rate': exchange_rate,
        'title': f'Edit Exchange Rate - {exchange_rate.currency_pair}',
        'submit_text': 'Update Exchange Rate'
    }
    return render(request, 'admin/exchange_rate_form.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
def admin_delete_exchange_rate(request, pk):
    """Delete exchange rate"""
    exchange_rate = get_object_or_404(ExchangeRate, pk=pk)
    
    if request.method == 'POST':
        currency_pair = exchange_rate.currency_pair
        exchange_rate.delete()
        messages.success(request, f'Exchange rate "{currency_pair}" has been deleted successfully.')
        return redirect('news:admin_exchange_rates')
    
    context = {
        'object': exchange_rate,
        'object_type': 'Exchange Rate',
        'object_name': exchange_rate.currency_pair
    }
    return render(request, 'admin/confirm_delete.html', context)


@user_passes_test(is_admin_user, login_url='news:admin_login')
@require_http_methods(["POST"])
def admin_toggle_exchange_rate_status(request, pk):
    """Toggle exchange rate active status via AJAX"""
    exchange_rate = get_object_or_404(ExchangeRate, pk=pk)
    exchange_rate.is_active = not exchange_rate.is_active
    exchange_rate.save()
    
    return JsonResponse({
        'success': True,
        'is_active': exchange_rate.is_active,
        'message': f'Exchange rate status updated to {"Active" if exchange_rate.is_active else "Inactive"}'
    })
