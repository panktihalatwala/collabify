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
    ("Priya Sharma", "fashion", 2100000),
    ("Rahul Verma", "tech", 850000),
    ("Ananya Singh", "beauty", 1500000),
    ("Arjun Kapoor", "fitness", 3200000),
    ("Meera Nair", "food", 680000),
]):
    first, last = name.split()
    username = f"{first.lower()}{last.lower()}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password="demo1234", role='influencer',
            first_name=first, last_name=last,
            email=f"{username}@demo.com",
            location="India"
        )
        InfluencerProfile.objects.create(
            user=user, niche=niche, followers_count=followers,
            engagement_rate=round(2.5 + i * 0.8, 2),
            collab_price_min=5000 + i * 2000,
            collab_price_max=50000 + i * 10000,
            languages='Hindi, English',
            avg_rating=round(4.2 + i * 0.1, 2),
            total_reviews=10 + i * 5,
        )
        print(f"  Created influencer: {username}")

# Brands
for company, industry in [
    ("Myntra India", "fashion"),
    ("Boat Lifestyle", "tech"),
    ("Nykaa", "beauty"),
    ("HealthifyMe", "health"),
]:
    username = company.lower().replace(" ", "").replace(".", "")
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password="demo1234", role='brand',
            first_name=company, email=f"{username}@demo.com",
            location="India"
        )
        brand = BrandProfile.objects.create(
            user=user, company_name=company, industry=industry
        )
        Campaign.objects.create(
            brand=brand,
            title=f"{company} Festive Season Campaign 2024",
            description=f"Looking for talented Indian creators to promote our {industry} products this festive season.",
            budget=80000 + len(company) * 1000,
            deadline=date.today() + timedelta(days=30),
            status='open',
            influencer_count=3,
            required_niche=industry,
            platforms="Instagram, YouTube",
        )
        print(f"  Created brand: {username}")

print("\nDone!")
print("Influencer login: priyasharma / demo1234")
print("Brand login: myntraindia / demo1234")
print("Admin: http://127.0.0.1:8000/admin/")