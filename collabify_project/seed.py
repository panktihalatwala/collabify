import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collabify.settings')
django.setup()

from accounts.models import User
from influencers.models import InfluencerProfile
from brands.models import BrandProfile
from campaigns.models import Campaign
from datetime import date, timedelta

print("Creating demo users...")

# Influencers
for i, (name, niche, followers) in enumerate([
    ("Sarah Johnson", "fashion", 2100000),
    ("Mike Chen", "tech", 850000),
    ("Priya Sharma", "beauty", 1500000),
    ("Alex Rivera", "fitness", 3200000),
    ("Emma Davis", "food", 680000),
]):
    first, last = name.split()
    username = f"{first.lower()}{last.lower()}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password="demo1234", role='influencer',
                                         first_name=first, last_name=last, email=f"{username}@demo.com")
        InfluencerProfile.objects.create(
            user=user, niche=niche, followers_count=followers,
            engagement_rate=round(2.5 + i * 0.8, 2),
            collab_price_min=500 + i * 200, collab_price_max=5000 + i * 1000,
            avg_rating=round(4.2 + i * 0.1, 2), total_reviews=10 + i * 5,
        )
        print(f"  Created influencer: {username}")

# Brands
for company, industry in [
    ("Nike Digital", "sports"), ("TechStart Inc", "tech"),
    ("Glow Beauty", "beauty"), ("FitLife Co", "health"),
]:
    username = company.lower().replace(" ", "").replace(".", "")
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password="demo1234", role='brand',
                                         first_name=company, email=f"{username}@demo.com")
        brand = BrandProfile.objects.create(user=user, company_name=company, industry=industry)
        Campaign.objects.create(
            brand=brand, title=f"{company} Summer Campaign 2024",
            description=f"Looking for talented creators to promote our {industry} products this summer.",
            budget=8000 + len(company) * 100,
            deadline=date.today() + timedelta(days=30),
            status='open', influencer_count=3,
            required_niche=industry, platforms="Instagram, TikTok",
        )
        print(f"  Created brand: {username}")

print("\nDone! Login at http://127.0.0.1:8000/accounts/login/")
print("Any influencer: username=sarahjohnson, password=demo1234")
print("Any brand: username=nikedigital, password=demo1234")
print("Admin: http://127.0.0.1:8000/admin/")