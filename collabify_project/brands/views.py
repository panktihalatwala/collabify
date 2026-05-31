from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import BrandProfile, Bookmark
from .forms import BrandProfileForm
from influencers.models import InfluencerProfile

def brand_detail(request, pk):
    profile = get_object_or_404(BrandProfile, pk=pk)
    from campaigns.models import Campaign
    campaigns = Campaign.objects.filter(brand=profile).order_by('-created_at')
    return render(request, 'brands/detail.html', {'profile': profile, 'campaigns': campaigns})

@login_required
def create_profile(request):
    if hasattr(request.user, 'brand_profile'):
        return redirect('brands:detail', pk=request.user.brand_profile.pk)
    if request.method == 'POST':
        form = BrandProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Brand profile created!')
            return redirect('dashboard:home')
    else:
        form = BrandProfileForm()
    return render(request, 'brands/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(BrandProfile, user=request.user)
    if request.method == 'POST':
        form = BrandProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('brands:detail', pk=profile.pk)
    else:
        form = BrandProfileForm(instance=profile)
    return render(request, 'brands/edit_profile.html', {'form': form})

@login_required
def toggle_bookmark(request, influencer_pk):
    if not request.user.is_brand():
        return JsonResponse({'error': 'Brands only'}, status=403)
    brand = get_object_or_404(BrandProfile, user=request.user)
    influencer = get_object_or_404(InfluencerProfile, pk=influencer_pk)
    bookmark, created = Bookmark.objects.get_or_create(brand=brand, influencer=influencer)
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})
    return JsonResponse({'bookmarked': True})

@login_required
def bookmarks_list(request):
    brand = get_object_or_404(BrandProfile, user=request.user)
    bookmarks = brand.bookmarks.select_related('influencer__user').all()
    return render(request, 'brands/bookmarks.html', {'bookmarks': bookmarks})