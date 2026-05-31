from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from influencers.models import InfluencerProfile
from brands.models import BrandProfile

@login_required
def leave_review_influencer(request, pk):
    influencer = get_object_or_404(InfluencerProfile, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.influencer = influencer
            review.save()
            reviews = influencer.reviews.all()
            influencer.avg_rating = round(
                sum(r.rating for r in reviews) / reviews.count(), 2
            )
            influencer.total_reviews = reviews.count()
            influencer.save()
            messages.success(request, 'Review submitted!')
            return redirect('influencers:detail', pk=influencer.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/leave_review.html', {
        'form': form,
        'target': influencer,
        'target_type': 'influencer'
    })

@login_required
def leave_review_brand(request, pk):
    brand = get_object_or_404(BrandProfile, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.brand = brand
            review.save()
            reviews = brand.reviews.all()
            brand.avg_rating = round(
                sum(r.rating for r in reviews) / reviews.count(), 2
            )
            brand.save()
            messages.success(request, 'Review submitted!')
            return redirect('brands:detail', pk=brand.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/leave_review.html', {
        'form': form,
        'target': brand,
        'target_type': 'brand'
    })