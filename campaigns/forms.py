from django import forms
from .models import Campaign, CampaignApplication, CollaborationRequest

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white/80'
TEXTAREA_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white/80 resize-none'

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['brand', 'status', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Campaign title'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'budget': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Budget in ₹'}),
            'target_audience': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'required_niche': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. fashion, fitness'}),
            'platforms': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Instagram, YouTube, Twitter'}),
            'deliverables': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3}),
            'deadline': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'influencer_count': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'hashtags': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '#hashtag1 #hashtag2'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = CampaignApplication
        fields = ['message', 'proposed_rate']
        widgets = {
            'message': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Why are you a great fit?'}),
            'proposed_rate': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Your rate (₹)'}),
        }

class CollaborationRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        brand = kwargs.pop('brand', None)
        super().__init__(*args, **kwargs)
        if brand:
            from .models import Campaign
            self.fields['campaign'].queryset = Campaign.objects.filter(brand=brand, status='open')

    class Meta:
        model = CollaborationRequest
        fields = ['campaign', 'message', 'payment_amount', 'deadline']
        widgets = {
            'campaign': forms.Select(attrs={'class': INPUT_CLASS}),
            'message': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'payment_amount': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Amount in ₹'}),
            'deadline': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
        }