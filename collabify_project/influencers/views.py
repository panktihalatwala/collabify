from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import InfluencerProfile, NICHE_CHOICES
from .forms import InfluencerProfileForm

def influencer_list(request):
    profiles = InfluencerProfile.objects.select_related('user').all()
    niche = request.GET.get('niche', '')
    platform = request.GET.get('platform', '')
    min_followers = request.GET.get('min_followers', '')
    max_followers = request.GET.get('max_followers', '')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '-followers_count')

    if niche:
        profiles = profiles.filter(niche=niche)
    if min_followers:
        profiles = profiles.filter(followers_count__gte=int(min_followers))
    if max_followers:
        profiles = profiles.filter(followers_count__lte=int(max_followers))
    if search:
        profiles = profiles.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__bio__icontains=search) |
            Q(niche__icontains=search)
        )
    valid_sorts = ['-followers_count', 'followers_count', '-avg_rating', '-engagement_rate', '-created_at']
    if sort in valid_sorts:
        profiles = profiles.order_by(sort)

    return render(request, 'influencers/list.html', {
        'profiles': profiles,
        'niche_choices': NICHE_CHOICES,
        'selected_niche': niche,
        'search': search,
        'sort': sort,
    })

def influencer_detail(request, pk):
    profile = get_object_or_404(InfluencerProfile, pk=pk)
    from reviews.models import Review
    from campaigns.models import CollaborationRequest
    reviews = Review.objects.filter(influencer=profile).select_related('reviewer').order_by('-created_at')
    is_bookmarked = False
    if request.user.is_authenticated and request.user.is_brand_user:
        from brands.models import Bookmark
        is_bookmarked = Bookmark.objects.filter(brand__user=request.user, influencer=profile).exists()
    return render(request, 'influencers/detail.html', {
        'profile': profile,
        'reviews': reviews,
        'is_bookmarked': is_bookmarked,
    })

@login_required
def create_profile(request):
    if hasattr(request.user, 'influencer_profile'):
        return redirect('influencers:detail', pk=request.user.influencer_profile.pk)
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('dashboard:home')
    else:
        form = InfluencerProfileForm()
    return render(request, 'influencers/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(InfluencerProfile, user=request.user)
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('influencers:detail', pk=profile.pk)
    else:
        form = InfluencerProfileForm(instance=profile)
    return render(request, 'influencers/edit_profile.html', {'form': form, 'profile': profile})