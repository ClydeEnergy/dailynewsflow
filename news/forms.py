from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import NewsArticle, Country, NewsProvider, MarketTicker, Commodity, Cryptocurrency, SocialMediaPost


class NewsArticleForm(forms.ModelForm):
    """Form for creating and editing news articles"""
    
    class Meta:
        model = NewsArticle
        fields = ['title', 'country', 'news_provider', 'image', 'link', 'description', 'date_posted', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title',
                'required': True
            }),
            'country': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'news_provider': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL',
                'required': True
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article URL',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter article description'
            }),
            'date_posted': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date_posted to now if creating new article
        if not self.instance.pk:
            self.initial['date_posted'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
            self.initial['is_active'] = True
        
        # Filter active countries and providers
        self.fields['country'].queryset = Country.objects.filter(is_active=True).order_by('name')
        self.fields['news_provider'].queryset = NewsProvider.objects.filter(is_active=True).order_by('name')


class CountryForm(forms.ModelForm):
    """Form for creating and editing countries"""
    
    class Meta:
        model = Country
        fields = ['name', 'code', 'flag_url', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country name',
                'required': True
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 2-letter country code (e.g., US, GB)',
                'required': True,
                'maxlength': 2,
                'style': 'text-transform: uppercase;'
            }),
            'flag_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter flag image URL (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['is_active'] = True
    
    def clean_code(self):
        code = self.cleaned_data.get('code', '').upper()
        if len(code) != 2:
            raise forms.ValidationError("Country code must be exactly 2 letters.")
        return code


class NewsProviderForm(forms.ModelForm):
    """Form for creating and editing news providers"""
    
    class Meta:
        model = NewsProvider
        fields = ['name', 'website', 'country', 'logo_url', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news provider name',
                'required': True
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter provider website URL',
                'required': True
            }),
            'country': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'logo_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter logo image URL (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['is_active'] = True


class AdminLoginForm(forms.Form):
    """Custom admin login form"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': True,
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )


class AdminUserForm(forms.ModelForm):
    """Form for creating and editing admin users"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        required=False
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if not self.is_edit:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            self.initial['is_active'] = True
            self.initial['is_staff'] = True
        else:
            self.fields['password1'].help_text = "Leave blank to keep current password"
            self.fields['password2'].help_text = "Leave blank to keep current password"
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not self.is_edit and not password1:
            raise forms.ValidationError("Password is required for new users.")
        
        if password1 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk:
            # Editing existing user
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A user with this username already exists.")
        else:
            # Creating new user
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("A user with this username already exists.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user


class MarketTickerForm(forms.ModelForm):
    """Form for creating and editing market tickers"""
    
    class Meta:
        model = MarketTicker
        fields = ['symbol', 'company_name', 'exchange', 'current_price', 'price_change', 
                 'percentage_change', 'volume', 'market_cap', 'high_52_week', 'low_52_week', 'is_active']
        widgets = {
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., AAPL',
                'required': True
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Apple Inc.',
                'required': True
            }),
            'exchange': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., NASDAQ',
                'required': True
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'required': True
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'required': True
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'market_cap': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'high_52_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'low_52_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CommodityForm(forms.ModelForm):
    """Form for creating and editing commodities"""
    
    class Meta:
        model = Commodity
        fields = ['name', 'symbol', 'unit', 'current_price', 'price_change', 
                 'percentage_change', 'exchange', 'high_52_week', 'low_52_week', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Gold',
                'required': True
            }),
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., XAU',
                'required': True
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., oz',
                'required': True
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'required': True
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'required': True
            }),
            'exchange': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., COMEX'
            }),
            'high_52_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'low_52_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CryptocurrencyForm(forms.ModelForm):
    """Form for creating and editing cryptocurrencies"""
    
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'current_price', 'price_change', 'percentage_change', 
                 'market_cap', 'volume_24h', 'circulating_supply', 'total_supply', 'ath', 'atl', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bitcoin',
                'required': True
            }),
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., BTC',
                'required': True
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'min': '0',
                'required': True
            }),
            'price_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'required': True
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'required': True
            }),
            'market_cap': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'volume_24h': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'circulating_supply': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'total_supply': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'ath': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'min': '0'
            }),
            'atl': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class SocialMediaPostForm(forms.ModelForm):
    """Form for creating and editing social media posts"""
    
    class Meta:
        model = SocialMediaPost
        fields = [
            'title', 'content', 'platform', 'author_name', 'author_handle',
            'post_url', 'image_url', 'likes', 'shares', 'comments',
            'is_featured', 'is_active', 'posted_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title or headline',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter post content or description',
                'required': True
            }),
            'platform': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author or account name',
                'required': True
            }),
            'author_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter social media handle (e.g., @username)'
            }),
            'post_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter direct link to the original post'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL to post image or media'
            }),
            'likes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'shares': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'comments': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default posted_at to current time if not provided
        if not self.instance.pk and not self.initial.get('posted_at'):
            self.fields['posted_at'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
