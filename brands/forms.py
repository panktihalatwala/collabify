from django import forms
from .models import BrandProfile

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white/80'

class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        exclude = ['user', 'avg_rating', 'total_campaigns', 'is_verified', 'created_at']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Company Name'}),
            'industry': forms.Select(attrs={'class': INPUT_CLASS}),
            'website': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://yourcompany.com'}),
            'company_size': forms.Select(attrs={'class': INPUT_CLASS}),
            'instagram_url': forms.URLInput(attrs={'class': INPUT_CLASS}),
            'linkedin_url': forms.URLInput(attrs={'class': INPUT_CLASS}),
            'twitter_url': forms.URLInput(attrs={'class': INPUT_CLASS}),
        }