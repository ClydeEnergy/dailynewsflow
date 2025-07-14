from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models import Country, NewsProvider, Category


class AdminLoginForm(forms.Form):
    """Form for admin login"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )


class AdminUserForm(UserCreationForm):
    """Form for creating and editing admin users"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    is_staff = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Add form-control class to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # If editing, make passwords optional
        if self.is_edit:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].help_text = 'Leave blank to keep current password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        
        if commit:
            # Only set password if it's provided (for edit forms)
            if self.cleaned_data.get('password1'):
                user.set_password(self.cleaned_data['password1'])
            user.save()
        return user


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
        fields = ['name', 'website', 'country', 'logo_url', 'is_active']
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
        # Filter to show only active countries
        self.fields['country'].queryset = Country.objects.filter(is_active=True).order_by('name')


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name (e.g., Politics, Business)',
                'required': True
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL-friendly version (e.g., politics, business)',
                'required': True,
                'pattern': '[a-z0-9-]+',
                'title': 'Only lowercase letters, numbers, and hyphens allowed'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the category'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'FontAwesome icon class (e.g., fas fa-newspaper)',
                'required': True
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'title': 'Choose category color'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['is_active'] = True
            self.initial['color'] = '#007bff'
            self.initial['icon'] = 'fas fa-newspaper'
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').lower()
        if not slug:
            raise forms.ValidationError("Slug is required.")
        
        # Check for valid characters
        import re
        if not re.match(r'^[a-z0-9-]+$', slug):
            raise forms.ValidationError("Slug can only contain lowercase letters, numbers, and hyphens.")
        
        # Check for uniqueness (excluding current instance if editing)
        existing = Category.objects.filter(slug=slug)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("A category with this slug already exists.")
        
        return slug
    
    def clean_color(self):
        color = self.cleaned_data.get('color', '')
        if color and not color.startswith('#'):
            color = '#' + color
        if len(color) != 7:
            raise forms.ValidationError("Please enter a valid hex color code.")
        return color
