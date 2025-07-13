from django.db import models
from django.urls import reverse
from django.utils import timezone


class Country(models.Model):
    """Model to store country information"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True, help_text="ISO 3166-1 alpha-2 country code")
    flag_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Model to store article categories"""
    name = models.CharField(max_length=100, unique=True, help_text="Category name (e.g., Politics, Business, Technology)")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly version of the name")
    description = models.TextField(blank=True, help_text="Brief description of the category")
    icon = models.CharField(max_length=50, default='fas fa-newspaper', help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code for the category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:category', kwargs={'slug': self.slug})


class NewsProvider(models.Model):
    """Model to store news provider information"""
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField()
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='news_providers', help_text="Country where this provider is based")
    logo_url = models.URLField(blank=True, null=True, help_text="URL to provider logo")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """Simplified model for posting news articles"""
    title = models.CharField(max_length=255, help_text="Article headline")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', null=True, blank=True, help_text="Article category")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='articles')
    news_provider = models.ForeignKey(NewsProvider, on_delete=models.CASCADE, related_name='articles')
    image = models.URLField(help_text="URL to article image")
    link = models.URLField(help_text="Link to the full article")
    date_posted = models.DateTimeField(default=timezone.now, help_text="Date when article was posted")
    
    # Additional fields for better functionality
    description = models.TextField(blank=True, help_text="Brief description of the article")
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_posted']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return f"{self.title} - {self.country.name}"

    def get_absolute_url(self):
        return self.link

    def increment_views(self):
        """Increment the view count for this article"""
        self.views += 1
        self.save(update_fields=['views'])


from django.db import models
from django.core.validators import MinValueValidator

class MarketTicker(models.Model):
    CURRENCY_CHOICES = [
        ('AED', 'United Arab Emirates Dirham'),
        ('AUD', 'Australian Dollar'),
        ('BRL', 'Brazilian Real'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CLP', 'Chilean Peso'),
        ('CNY', 'Chinese Yuan'),
        ('CZK', 'Czech Koruna'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('HKD', 'Hong Kong Dollar'),
        ('HUF', 'Hungarian Forint'),
        ('IDR', 'Indonesian Rupiah'),
        ('ILS', 'Israeli New Shekel'),
        ('INR', 'Indian Rupee'),
        ('JPY', 'Japanese Yen'),
        ('KRW', 'South Korean Won'),
        ('MXN', 'Mexican Peso'),
        ('MYR', 'Malaysian Ringgit'),
        ('NOK', 'Norwegian Krone'),
        ('NZD', 'New Zealand Dollar'),
        ('PHP', 'Philippine Peso'),
        ('PKR', 'Pakistani Rupee'),
        ('PLN', 'Polish Zloty'),
        ('RUB', 'Russian Ruble'),
        ('SAR', 'Saudi Riyal'),
        ('SEK', 'Swedish Krona'),
        ('SGD', 'Singapore Dollar'),
        ('THB', 'Thai Baht'),
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
        ('VND', 'Vietnamese Dong'),
        ('ZAR', 'South African Rand'),
        ('ZIG', 'Zimbabwean Dollar'),
   ]

    # Core Identification
    symbol = models.CharField(
        max_length=10, 
        unique=True, 
        help_text="Stock symbol (e.g., AAPL, TSLA)"
    )
    company_name = models.CharField(
        max_length=200, 
        help_text="Full company name"
    )
    exchange = models.CharField(
        max_length=50, 
        help_text="Stock exchange (e.g., NYSE, NASDAQ)"
    )
    details_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to view more details about this ticker"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="USD",
        help_text="Currency code for all monetary values"
    )

    # Pricing Data
    current_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text="Current trading price"
    )
    price_change = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Net price change from previous close"
    )
    percentage_change = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        help_text="Percentage change from previous close"
    )

    # Volume and Market Cap
    volume = models.BigIntegerField(
        default=0, 
        help_text="Total shares traded today"
    )
    market_cap = models.BigIntegerField(
        null=True, 
        blank=True, 
        help_text="Market capitalization in currency units"
    )

    # 52-Week Range
    high_52_week = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="52-week high price"
    )
    low_52_week = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="52-week low price"
    )

    # Metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the ticker is currently active"
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last data update"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of record creation"
    )

    class Meta:
        ordering = ['symbol']
        verbose_name = "Market Ticker"
        verbose_name_plural = "Market Tickers"
        indexes = [
            models.Index(fields=['symbol']),
            models.Index(fields=['exchange']),
        ]

    def __str__(self):
        return f"{self.symbol} ({self.exchange}) - {self.company_name}"

    # ---- Derived Properties ----
    @property
    def is_positive_change(self):
        """Returns True if price change is non-negative."""
        return self.price_change >= 0

    @property
    def formatted_price_change(self):
        """Returns price change with +/- sign (e.g., '+5.25')."""
        sign = "+" if self.price_change >= 0 else ""
        return f"{sign}{self.price_change:.2f}"

    @property
    def formatted_percentage_change(self):
        """Returns percentage change with +/- sign (e.g., '+1.50%')."""
        sign = "+" if self.percentage_change >= 0 else ""
        return f"{sign}{self.percentage_change:.2f}%"

    @property
    def formatted_market_cap(self):
        """Returns market cap in human-readable format (e.g., '1.2B')."""
        if not self.market_cap:
            return "N/A"
        return f"{(self.market_cap / 1_000_000_000):.1f}B" if self.market_cap >= 1_000_000_000 else f"{(self.market_cap / 1_000_000):.1f}M"

class Commodity(models.Model):
    """Model to store commodity information"""
    name = models.CharField(max_length=100, unique=True, help_text="Commodity name (e.g., Gold, Oil, Silver)")
    symbol = models.CharField(max_length=10, help_text="Commodity symbol (e.g., XAU, WTI, XAG)")
    unit = models.CharField(max_length=50, help_text="Unit of measurement (e.g., oz, barrel, lb)")
    current_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Current commodity price")
    price_change = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price change from previous close")
    percentage_change = models.DecimalField(max_digits=6, decimal_places=2, help_text="Percentage change")
    exchange = models.CharField(max_length=50, blank=True, help_text="Primary exchange")
    high_52_week = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    low_52_week = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def is_positive_change(self):
        return self.price_change >= 0

    @property
    def formatted_price_change(self):
        sign = "+" if self.price_change >= 0 else ""
        return f"{sign}{self.price_change}"

    @property
    def formatted_percentage_change(self):
        sign = "+" if self.percentage_change >= 0 else ""
        return f"{sign}{self.percentage_change}%"


class Cryptocurrency(models.Model):
    """Model to store cryptocurrency information"""
    name = models.CharField(max_length=100, help_text="Cryptocurrency name (e.g., Bitcoin, Ethereum)")
    symbol = models.CharField(max_length=10, unique=True, help_text="Crypto symbol (e.g., BTC, ETH)")
    current_price = models.DecimalField(max_digits=15, decimal_places=8, help_text="Current crypto price in USD")
    price_change = models.DecimalField(max_digits=15, decimal_places=8, help_text="Price change from previous close")
    percentage_change = models.DecimalField(max_digits=6, decimal_places=2, help_text="Percentage change")
    market_cap = models.BigIntegerField(null=True, blank=True, help_text="Market capitalization in USD")
    volume_24h = models.BigIntegerField(default=0, help_text="24-hour trading volume")
    circulating_supply = models.BigIntegerField(null=True, blank=True, help_text="Circulating supply")
    total_supply = models.BigIntegerField(null=True, blank=True, help_text="Total supply")
    ath = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True, help_text="All-time high")
    atl = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True, help_text="All-time low")
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-market_cap']
        verbose_name = "Cryptocurrency"
        verbose_name_plural = "Cryptocurrencies"

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def is_positive_change(self):
        return self.price_change >= 0

    @property
    def formatted_price_change(self):
        sign = "+" if self.price_change >= 0 else ""
        return f"{sign}{self.price_change}"

    @property
    def formatted_percentage_change(self):
        sign = "+" if self.percentage_change >= 0 else ""
        return f"{sign}{self.percentage_change}%"


class SocialMediaPost(models.Model):
    """Model to store social media posts for display on the home page"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255, help_text="Post title or headline")
    content = models.TextField(help_text="Post content or description")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other', help_text="Social media platform")
    author_name = models.CharField(max_length=100, help_text="Author or account name")
    author_handle = models.CharField(max_length=100, blank=True, help_text="Social media handle (e.g., @username)")
    post_url = models.URLField(blank=True, help_text="Direct link to the original post")
    image_url = models.URLField(blank=True, help_text="URL to post image or media")
    
    # Engagement metrics
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes")
    shares = models.PositiveIntegerField(default=0, help_text="Number of shares")
    comments = models.PositiveIntegerField(default=0, help_text="Number of comments")
    
    # Meta fields
    is_featured = models.BooleanField(default=False, help_text="Show this post prominently")
    is_active = models.BooleanField(default=True, help_text="Display this post on the site")
    posted_at = models.DateTimeField(default=timezone.now, help_text="When the post was originally published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_at']
        verbose_name = "Social Media Post"
        verbose_name_plural = "Social Media Posts"

    def __str__(self):
        return f"{self.title} - {self.platform.title()}"

    @property
    def platform_icon(self):
        """Return the appropriate icon class for the platform"""
        icons = {
            'facebook': 'fab fa-facebook-f',
            'twitter': 'fab fa-twitter',
            'instagram': 'fab fa-instagram',
            'linkedin': 'fab fa-linkedin-in',
            'youtube': 'fab fa-youtube',
            'tiktok': 'fab fa-tiktok',
            'other': 'fas fa-share-alt'
        }
        return icons.get(self.platform, 'fas fa-share-alt')

    @property
    def platform_color(self):
        """Return the appropriate color class for the platform"""
        colors = {
            'facebook': '#1877F2',
            'twitter': '#1DA1F2',
            'instagram': '#E4405F',
            'linkedin': '#0A66C2',
            'youtube': '#FF0000',
            'tiktok': '#000000',
            'other': '#6c757d'
        }
        return colors.get(self.platform, '#6c757d')

    @property
    def total_engagement(self):
        """Calculate total engagement (likes + shares + comments)"""
        return self.likes + self.shares + self.comments

    def get_absolute_url(self):
        return self.post_url if self.post_url else '#'
    
class ExchangeRate(models.Model):
    """Model to store currency exchange rates"""
    MARKET_CHOICES = [
        ('forex', 'FOREX'),
        ('crypto', 'Crypto'),
        ('stocks', 'Stocks'),
        ('commodities', 'Commodities'),
    ]
    
    # Currency pair information
    base_currency = models.CharField(
        max_length=3, 
        help_text="Base currency code (e.g., USD, EUR)"
    )
    quote_currency = models.CharField(
        max_length=3, 
        help_text="Quote currency code (e.g., USD, EUR)"
    )
    currency_pair = models.CharField(
        max_length=10, 
        unique=True,
        help_text="Currency pair (e.g., EUR/USD, GBP/USD)"
    )
    description = models.CharField(
        max_length=100,
        help_text="Description of the currency pair (e.g., Euro to Dollar)"
    )
    
    # Market information
    market = models.CharField(
        max_length=20,
        choices=MARKET_CHOICES,
        default='forex',
        help_text="Market type"
    )
    
    # Rate data
    current_rate = models.DecimalField(
        max_digits=12, 
        decimal_places=6, 
        help_text="Current exchange rate"
    )
    rate_change = models.DecimalField(
        max_digits=10, 
        decimal_places=6, 
        help_text="Rate change from previous close"
    )
    percentage_change = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        help_text="Percentage change from previous close"
    )
    
    # Additional data
    high_24h = models.DecimalField(
        max_digits=12, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="24-hour high rate"
    )
    low_24h = models.DecimalField(
        max_digits=12, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="24-hour low rate"
    )
    
    # Metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the exchange rate is currently active"
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last data update"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of record creation"
    )

    class Meta:
        ordering = ['currency_pair']
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        indexes = [
            models.Index(fields=['currency_pair']),
            models.Index(fields=['market']),
        ]

    def __str__(self):
        return f"{self.currency_pair} - {self.current_rate}"

    def save(self, *args, **kwargs):
        # Auto-generate currency_pair if not provided
        if not self.currency_pair:
            self.currency_pair = f"{self.base_currency}/{self.quote_currency}"
        super().save(*args, **kwargs)

    @property
    def is_positive_change(self):
        """Returns True if rate change is non-negative."""
        return self.rate_change >= 0

    @property
    def formatted_rate_change(self):
        """Returns rate change with +/- sign."""
        sign = "+" if self.rate_change >= 0 else ""
        return f"{sign}{self.rate_change:.6f}"

    @property
    def formatted_percentage_change(self):
        """Returns percentage change with +/- sign."""
        sign = "+" if self.percentage_change >= 0 else ""
        return f"{sign}{self.percentage_change:.2f}%"

    @property
    def market_badge_color(self):
        """Returns color for market badge"""
        colors = {
            'forex': 'linear-gradient(45deg, #f39c12, #e67e22)',
            'crypto': 'linear-gradient(45deg, #9b59b6, #8e44ad)',
            'stocks': 'linear-gradient(45deg, #3498db, #2980b9)',
            'commodities': 'linear-gradient(45deg, #e74c3c, #c0392b)',
        }
        return colors.get(self.market, '#6c757d')
