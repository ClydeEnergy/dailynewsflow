from django.urls import path
from .views import (HomeView, about_view, contact_view, ArticleDetailView, 
                   CategoryView, SearchView, MarketDetailView, CountryView, 
                   ProviderView, filter_articles, get_article_stats, AllNewsView, 
                   SocialMediaView, AllSocialPostsView, MarketsView)
from . import admin_views

app_name = 'news'

urlpatterns = [
    # Main pages
    path('', HomeView.as_view(), name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('search/', SearchView.as_view(), name='search'),
    path('news/', AllNewsView.as_view(), name='all_news'),
    path('markets/', MarketsView.as_view(), name='markets'),
    path('social/', SocialMediaView.as_view(), name='social_media'),
    path('social/all/', AllSocialPostsView.as_view(), name='all_social_posts'),
    
    # Article detail
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    
    # Category view
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    
    # Country and provider views
    path('country/<str:code>/', CountryView.as_view(), name='country'),
    path('provider/<int:pk>/', ProviderView.as_view(), name='provider'),
    
    # API endpoints
    path('api/articles/', filter_articles, name='filter_articles'),
    path('api/statistics/', get_article_stats, name='get_article_stats'),
    
    # Custom Admin URLs
    path('admin/login/', admin_views.admin_login, name='admin_login'),
    path('admin/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Articles Management
    path('admin/articles/', admin_views.admin_articles, name='admin_articles'),
    path('admin/articles/add/', admin_views.admin_add_article, name='admin_add_article'),
    path('admin/articles/<int:pk>/edit/', admin_views.admin_edit_article, name='admin_edit_article'),
    path('admin/articles/<int:pk>/delete/', admin_views.admin_delete_article, name='admin_delete_article'),
    path('admin/articles/<int:pk>/toggle-status/', admin_views.admin_toggle_article_status, name='admin_toggle_article_status'),
    
    # Countries Management
    path('admin/countries/', admin_views.admin_countries, name='admin_countries'),
    path('admin/countries/add/', admin_views.admin_add_country, name='admin_add_country'),
    path('admin/countries/<int:pk>/edit/', admin_views.admin_edit_country, name='admin_edit_country'),
    
    # Providers Management
    path('admin/providers/', admin_views.admin_providers, name='admin_providers'),
    path('admin/providers/add/', admin_views.admin_add_provider, name='admin_add_provider'),
    path('admin/providers/<int:pk>/edit/', admin_views.admin_edit_provider, name='admin_edit_provider'),
    
    # Categories Management
    path('admin/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin/categories/add/', admin_views.admin_add_category, name='admin_add_category'),
    path('admin/categories/<int:pk>/edit/', admin_views.admin_edit_category, name='admin_edit_category'),
    path('admin/categories/<int:pk>/delete/', admin_views.admin_delete_category, name='admin_delete_category'),
    path('admin/categories/<int:pk>/toggle-status/', admin_views.admin_toggle_category_status, name='admin_toggle_category_status'),
    
    # Market Tickers Management
    path('admin/market-tickers/', admin_views.admin_market_tickers, name='admin_market_tickers'),
    path('admin/market-tickers/add/', admin_views.admin_add_market_ticker, name='admin_add_market_ticker'),
    path('admin/market-tickers/<int:pk>/edit/', admin_views.admin_edit_market_ticker, name='admin_edit_market_ticker'),
    path('admin/market-tickers/<int:pk>/delete/', admin_views.admin_delete_market_ticker, name='admin_delete_market_ticker'),
    path('market/<slug:slug>/', MarketDetailView.as_view(), name='market_detail'),
    

    # Commodities Management
    path('admin/commodities/', admin_views.admin_commodities, name='admin_commodities'),
    path('admin/commodities/add/', admin_views.admin_add_commodity, name='admin_add_commodity'),
    path('admin/commodities/<int:pk>/edit/', admin_views.admin_edit_commodity, name='admin_edit_commodity'),
    path('admin/commodities/<int:pk>/delete/', admin_views.admin_delete_commodity, name='admin_delete_commodity'),
    
    # Cryptocurrencies Management
    path('admin/cryptocurrencies/', admin_views.admin_cryptocurrencies, name='admin_cryptocurrencies'),
    path('admin/cryptocurrencies/add/', admin_views.admin_add_cryptocurrency, name='admin_add_cryptocurrency'),
    path('admin/cryptocurrencies/<int:pk>/edit/', admin_views.admin_edit_cryptocurrency, name='admin_edit_cryptocurrency'),
    path('admin/cryptocurrencies/<int:pk>/delete/', admin_views.admin_delete_cryptocurrency, name='admin_delete_cryptocurrency'),
    
    # User Management (Superuser only)
    path('admin/users/', admin_views.admin_users, name='admin_users'),
    path('admin/users/add/', admin_views.admin_add_user, name='admin_add_user'),
    path('admin/users/<int:pk>/edit/', admin_views.admin_edit_user, name='admin_edit_user'),
    path('admin/users/<int:pk>/delete/', admin_views.admin_delete_user, name='admin_delete_user'),
    
    # Social Media Posts Management
    path('admin/social-posts/', admin_views.admin_social_posts, name='admin_social_posts'),
    path('admin/social-posts/add/', admin_views.admin_add_social_post, name='admin_add_social_post'),
    path('admin/social-posts/<int:pk>/edit/', admin_views.admin_edit_social_post, name='admin_edit_social_post'),
    path('admin/social-posts/<int:pk>/delete/', admin_views.admin_delete_social_post, name='admin_delete_social_post'),
    path('admin/social-posts/<int:pk>/toggle-status/', admin_views.admin_toggle_social_post_status, name='admin_toggle_social_post_status'),
    path('admin/social-posts/<int:pk>/toggle-featured/', admin_views.admin_toggle_social_post_featured, name='admin_toggle_social_post_featured'),
    
    # Exchange Rates Management
    path('admin/exchange-rates/', admin_views.admin_exchange_rates, name='admin_exchange_rates'),
    path('admin/exchange-rates/add/', admin_views.admin_add_exchange_rate, name='admin_add_exchange_rate'),
    path('admin/exchange-rates/<int:pk>/edit/', admin_views.admin_edit_exchange_rate, name='admin_edit_exchange_rate'),
    path('admin/exchange-rates/<int:pk>/delete/', admin_views.admin_delete_exchange_rate, name='admin_delete_exchange_rate'),
    path('admin/exchange-rates/<int:pk>/toggle-status/', admin_views.admin_toggle_exchange_rate_status, name='admin_toggle_exchange_rate_status'),
]
