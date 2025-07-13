from django import forms
from ..models import ExchangeRate


class ExchangeRateForm(forms.ModelForm):
    """Form for creating and editing exchange rates"""
    
    class Meta:
        model = ExchangeRate
        fields = [
            'base_currency', 'quote_currency', 'description', 
            'market', 'current_rate', 'rate_change', 'percentage_change', 
            'high_24h', 'low_24h', 'is_active'
        ]
        widgets = {
            'base_currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Base Currency (e.g., EUR)',
                'maxlength': '3'
            }),
            'quote_currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quote Currency (e.g., USD)',
                'maxlength': '3'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description (e.g., Euro to Dollar)'
            }),
            'market': forms.Select(attrs={
                'class': 'form-control'
            }),
            'current_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': '0.000000'
            }),
            'rate_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': '0.000000',
                'value': '0.000000'
            }),
            'percentage_change': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
                'value': '0.00'
            }),
            'high_24h': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': '0.000000'
            }),
            'low_24h': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': '0.000000'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for new forms
        if not self.instance.pk:
            self.fields['rate_change'].initial = 0.000000
            self.fields['percentage_change'].initial = 0.00
            self.fields['is_active'].initial = True

    def clean_base_currency(self):
        base_currency = self.cleaned_data.get('base_currency')
        if base_currency:
            return base_currency.upper()
        return base_currency

    def clean_quote_currency(self):
        quote_currency = self.cleaned_data.get('quote_currency')
        if quote_currency:
            return quote_currency.upper()
        return quote_currency

    def clean(self):
        cleaned_data = super().clean()
        base_currency = cleaned_data.get('base_currency')
        quote_currency = cleaned_data.get('quote_currency')
        
        # Validate currency codes are provided
        if not base_currency:
            raise forms.ValidationError("Base currency is required.")
        if not quote_currency:
            raise forms.ValidationError("Quote currency is required.")
            
        # Ensure they're different
        if base_currency == quote_currency:
            raise forms.ValidationError("Base currency and quote currency must be different.")
            
        return cleaned_data