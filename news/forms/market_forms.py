from django import forms
from ..models import MarketTicker, Commodity, Cryptocurrency, SocialMediaPost


class MarketTickerForm(forms.ModelForm):
    """Form for creating and editing market tickers"""
    
    class Meta:
        model = MarketTicker
        fields = ['symbol', 'company_name', 'exchange', 'current_price', 'price_change', 'percentage_change', 'currency', 'details_link']
        widgets = {
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock Symbol (e.g., AAPL)'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'exchange': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exchange (e.g., NASDAQ)'
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'details_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
        }


class CommodityForm(forms.ModelForm):
    """Form for creating and editing commodities"""
    
    class Meta:
        model = Commodity
        fields = ['name', 'symbol', 'current_price', 'price_change', 'percentage_change', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Commodity Name (e.g., Gold)'
            }),
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Symbol (e.g., XAU)'
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unit (e.g., per ounce)'
            }),
        }


class CryptocurrencyForm(forms.ModelForm):
    """Form for creating and editing cryptocurrencies"""
    
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'current_price', 'price_change', 'percentage_change', 'market_cap', 'volume_24h']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cryptocurrency Name (e.g., Bitcoin)'
            }),
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Symbol (e.g., BTC)'
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'placeholder': '0.00'
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'placeholder': '0.00'
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'market_cap': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'volume_24h': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }


class SocialMediaPostForm(forms.ModelForm):
    """Form for creating and editing social media posts"""
    
    class Meta:
        model = SocialMediaPost
        fields = ['title', 'content', 'platform', 'author_name', 'author_handle', 'post_url', 'posted_at', 'is_active', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Post content...'
            }),
            'platform': forms.Select(attrs={
                'class': 'form-control'
            }),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author Name'
            }),
            'author_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'post_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
