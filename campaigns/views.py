from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Campaign, CampaignApplication, CollaborationRequest
from .forms import CampaignForm, ApplicationForm, CollaborationRequestForm
from brands.models import BrandProfile
from influencers.models import InfluencerProfile 
from .models import Campaign, CampaignApplication, CollaborationRequest, BookmarkedCampaign


def campaign_list(request):
    campaigns = Campaign.objects.filter(
        status='open'
    ).select_related('brand').order_by('-created_at')
    niche  = request.GET.get('niche', '')
    search = request.GET.get('search', '')
    if niche:
        campaigns = campaigns.filter(required_niche=niche)
    if search:
        campaigns = campaigns.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    return render(request, 'campaigns/list.html', {
        'campaigns': campaigns,
        'search': search
    })


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    already_applied = False
    if request.user.is_authenticated and request.user.role == 'influencer':
        already_applied = CampaignApplication.objects.filter(
            campaign=campaign,
            influencer__user=request.user
        ).exists()
    return render(request, 'campaigns/detail.html', {
        'campaign': campaign,
        'already_applied': already_applied,
        'app_form': ApplicationForm(),
    })


@login_required
def create_campaign(request):
    if request.user.role != 'brand':
        messages.error(request, 'Only brands can create campaigns.')
        return redirect('campaigns:list')
    brand = get_object_or_404(BrandProfile, user=request.user)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.brand = brand
            campaign.save()
            brand.total_campaigns += 1
            brand.save()
            messages.success(request, 'Campaign created successfully!')
            return redirect('campaigns:detail', pk=campaign.pk)
    else:
        form = CampaignForm()
    return render(request, 'campaigns/create.html', {'form': form})


@login_required
def apply_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.user.role != 'influencer':
        messages.error(request, 'Only influencers can apply.')
        return redirect('campaigns:detail', pk=pk)
    try:
        influencer = request.user.influencer_profile
    except Exception:
        messages.error(request, 'Please create your influencer profile first.')
        return redirect('influencers:create_profile')
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            if CampaignApplication.objects.filter(
                campaign=campaign,
                influencer=influencer
            ).exists():
                messages.warning(request, 'You already applied to this campaign.')
                return redirect('campaigns:detail', pk=pk)
            app = form.save(commit=False)
            app.campaign   = campaign
            app.influencer = influencer
            app.save()
            from notifications.models import Notification
            Notification.objects.create(
                user=campaign.brand.user,
                title='New Campaign Application',
                message=f'{request.user.get_full_name() or request.user.username} applied to "{campaign.title}"',
                notification_type='application',
                link=f'/campaigns/{campaign.pk}/'
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('campaigns:detail', pk=campaign.pk)
    return redirect('campaigns:detail', pk=campaign.pk)


@login_required
def my_campaigns(request):
    print(f"DEBUG: user={request.user.username} role={request.user.role}")
    
    if request.user.role == 'brand':
        print("DEBUG: going to brand campaigns")
        try:
            brand = BrandProfile.objects.get(user=request.user)
        except BrandProfile.DoesNotExist:
            messages.error(request, 'Please create your brand profile first.')
            return redirect('brands:create_profile')
        campaigns = Campaign.objects.filter(
            brand=brand
        ).order_by('-created_at')
        print(f"DEBUG: found {campaigns.count()} campaigns")
        return render(request, 'campaigns/my_campaigns.html', {
            'campaigns': campaigns
        })
    else:
        print("DEBUG: going to influencer applications")
        try:
            influencer = request.user.influencer_profile
        except Exception:
            messages.error(request, 'Please create your influencer profile first.')
            return redirect('influencers:create_profile')
        applications = CampaignApplication.objects.filter(
            influencer=influencer
        ).select_related('campaign__brand').order_by('-created_at')
        return render(request, 'campaigns/my_applications.html', {
            'applications': applications
        })

@login_required
def send_collab_request(request, influencer_pk):
    if request.user.role != 'brand':
        messages.error(request, 'Only brands can send requests.')
        return redirect('influencers:list')
    brand      = get_object_or_404(BrandProfile, user=request.user)
    influencer = get_object_or_404(InfluencerProfile, pk=influencer_pk)
    if request.method == 'POST':
        form = CollaborationRequestForm(request.POST, brand=brand)
        if form.is_valid():
            req            = form.save(commit=False)
            req.brand      = brand
            req.influencer = influencer
            req.save()
            from notifications.models import Notification
            Notification.objects.create(
                user=influencer.user,
                title='New Collaboration Request',
                message=f'{brand.company_name} sent you a collaboration request!',
                notification_type='collab_request',
                link='/dashboard/'
            )
            messages.success(request, 'Collaboration request sent!')
            return redirect('influencers:detail', pk=influencer.pk)
    else:
        form = CollaborationRequestForm(brand=brand)
    return render(request, 'campaigns/send_request.html', {
        'form': form,
        'influencer': influencer
    })


@login_required
def respond_collab(request, pk):
    collab = get_object_or_404(CollaborationRequest, pk=pk)
    if request.user != collab.influencer.user:
        messages.error(request, 'Not authorized.')
        return redirect('dashboard:home')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            collab.status = 'accepted'
            collab.save()
            from notifications.models import Notification
            Notification.objects.create(
                user=collab.brand.user,
                title='Collaboration Accepted!',
                message=f'{request.user.get_full_name() or request.user.username} accepted your collaboration request.',
                notification_type='accepted',
                link='/dashboard/'
            )
            messages.success(request, 'Collaboration accepted!')
        elif action == 'reject':
            collab.status = 'rejected'
            collab.save()
            from notifications.models import Notification
            Notification.objects.create(
                user=collab.brand.user,
                title='Collaboration Declined',
                message=f'{request.user.get_full_name() or request.user.username} declined your collaboration request.',
                notification_type='rejected',
                link='/dashboard/'
            )
            messages.info(request, 'Collaboration rejected.')
        elif action == 'counter':
            collab.status          = 'negotiating'
            collab.counter_offer   = request.POST.get('counter_offer')
            collab.counter_message = request.POST.get('counter_message', '')
            collab.save()
            messages.success(request, 'Counter offer sent!')
    return redirect('dashboard:home')

@login_required
def edit_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.brand.user != request.user:
        messages.error(request, 'Not authorized.')
        return redirect('campaigns:detail', pk=pk)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully!')
            return redirect('campaigns:detail', pk=campaign.pk)
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaigns/edit.html', {
        'form': form,
        'campaign': campaign
    })


@login_required
def delete_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.brand.user != request.user:
        messages.error(request, 'Not authorized.')
        return redirect('campaigns:detail', pk=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted successfully.')
        return redirect('campaigns:my_campaigns')
    return render(request, 'campaigns/delete_confirm.html', {
        'campaign': campaign
    })


@login_required
def change_campaign_status(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.brand.user != request.user:
        messages.error(request, 'Not authorized.')
        return redirect('campaigns:detail', pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pause':
            campaign.status = 'paused'
            messages.info(request, 'Campaign paused.')
        elif action == 'reopen':
            campaign.status = 'open'
            messages.success(request, 'Campaign reopened!')
        elif action == 'complete':
            campaign.status = 'completed'
            messages.success(request, 'Campaign marked as completed!')
        elif action == 'ongoing':
            campaign.status = 'ongoing'
            messages.success(request, 'Campaign marked as ongoing!')
        campaign.save()
    return redirect('campaigns:my_campaigns')

@login_required
def toggle_bookmark_campaign(request, pk):
    from django.http import JsonResponse
    if request.user.role != 'influencer':
        return JsonResponse({'error': 'Influencers only'}, status=403)
    try:
        influencer = request.user.influencer_profile
    except:
        return JsonResponse({'error': 'No profile'}, status=403)
    campaign = get_object_or_404(Campaign, pk=pk)
    bookmark, created = BookmarkedCampaign.objects.get_or_create(
        influencer=influencer,
        campaign=campaign
    )
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})
    return JsonResponse({'bookmarked': True})


@login_required
def saved_campaigns(request):
    if request.user.role != 'influencer':
        return redirect('campaigns:list')
    try:
        influencer = request.user.influencer_profile
    except:
        return redirect('influencers:create_profile')
    bookmarks = BookmarkedCampaign.objects.filter(
        influencer=influencer
    ).select_related('campaign__brand').order_by('-created_at')
    return render(request, 'campaigns/saved_campaigns.html', {
        'bookmarks': bookmarks
    })