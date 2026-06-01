from django import forms
from .models import InfluencerProfile

from django import forms
from .models import InfluencerProfile

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white/80'

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        exclude = ['user', 'avg_rating', 'total_reviews', 'total_collaborations', 'total_earnings', 'created_at']
        widgets = {
            'niche': forms.Select(attrs={'class': INPUT_CLASS}),
            'followers_count': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. 50000'}),
            'engagement_rate': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. 3.5'}),
            'collab_price_min': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Min price (₹)'}),
            'collab_price_max': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Max price (₹)'}),
            'languages': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. Hindi, English, Tamil'}),
            'instagram_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://instagram.com/...'}),
            'youtube_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://youtube.com/...'}),
            'twitter_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://twitter.com/...'}),
            'linkedin_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://linkedin.com/...'}),
            'website_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://yoursite.com'}),
        }