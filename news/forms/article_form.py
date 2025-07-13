from django import forms
from django.utils import timezone
from ..models import NewsArticle, Category

class NewsArticleForm(forms.ModelForm):
    """Form for creating and editing news articles with rich text support"""
    
    class Meta:
        model = NewsArticle
        fields = ['title', 'category', 'country', 'news_provider', 'image', 'link', 'description', 'date_posted', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': False
            }),
            'country': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'news_provider': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article URL',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rich-text-editor',
                'placeholder': 'Enter article description with formatting support...',
                'rows': 8,
                'id': 'rich-text-description'
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
        # Add empty option for category
        self.fields['category'].empty_label = "Select a category (optional)"
        self.fields['category'].queryset = Category.objects.all()
        
        # Add help text for rich text editor
        self.fields['description'].help_text = (
            "Use the rich text editor to format your description. "
            "You can add bullet points, bold text, italics, and more."
        )

    def clean_date_posted(self):
        date_posted = self.cleaned_data.get('date_posted')
        if not date_posted:
            date_posted = timezone.now()
        return date_posted
