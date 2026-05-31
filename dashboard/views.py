from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

@login_required
def home(request):
    user = request.user
    context = {}

    if user.is_influencer():
        try:
            profile = user.influencer_profile
        except:
            return redirect('influencers:create_profile')

        from campaigns.models import CampaignApplication, CollaborationRequest
        applications = CampaignApplication.objects.filter(
            influencer=profile).order_by('-created_at')
        collab_requests = CollaborationRequest.objects.filter(
            influencer=profile).order_by('-created_at')

        # Chart data
        from django.db.models import Count
        from django.utils import timezone
        import datetime
        months = []
        earnings_data = []
        for i in range(5, -1, -1):
            month = timezone.now() - datetime.timedelta(days=30*i)
            months.append(month.strftime('%b'))
            earnings_data.append(float(profile.total_earnings) / 6)

        context = {
            'profile': profile,
            'applications': applications[:5],
            'collab_requests': collab_requests[:5],
            'total_applications': applications.count(),
            'pending_requests': collab_requests.filter(status='pending').count(),
            'active_collabs': collab_requests.filter(status='accepted').count(),
            'chart_months': json.dumps(months),
            'chart_earnings': json.dumps(earnings_data),
        }

    elif user.is_brand():
        try:
            profile = user.brand_profile
        except:
            return redirect('brands:create_profile')

        from campaigns.models import Campaign, CampaignApplication, CollaborationRequest
        campaigns = Campaign.objects.filter(brand=profile).order_by('-created_at')
        applications = CampaignApplication.objects.filter(
            campaign__brand=profile).order_by('-created_at')
        sent_requests = CollaborationRequest.objects.filter(
            brand=profile).order_by('-created_at')

        # Chart data
        from django.utils import timezone
        import datetime
        months = []
        app_data = []
        for i in range(5, -1, -1):
            month = timezone.now() - datetime.timedelta(days=30*i)
            months.append(month.strftime('%b'))
            app_data.append(applications.filter(
                created_at__month=month.month,
                created_at__year=month.year
            ).count())

        context = {
            'profile': profile,
            'campaigns': campaigns[:5],
            'applications': applications[:5],
            'sent_requests': sent_requests[:5],
            'total_campaigns': campaigns.count(),
            'open_campaigns': campaigns.filter(status='open').count(),
            'total_applications': applications.count(),
            'chart_months': json.dumps(months),
            'chart_app_data': json.dumps(app_data),
        }

    notifs = user.notifications.filter(is_read=False)[:5]
    context['notifications'] = notifs

    return render(request, 'dashboard/home.html', context)