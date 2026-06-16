from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from influencers.models import InfluencerProfile
from brands.models import BrandProfile
from campaigns.models import CollaborationRequest


def has_completed_collab_with_influencer(user, influencer):
    """Check if brand has a completed collaboration with this influencer"""
    return CollaborationRequest.objects.filter(
        brand__user=user,
        influencer=influencer,
        status='completed'
    ).exists()


def has_completed_collab_with_brand(user, brand):
    """Check if influencer has a completed collaboration with this brand"""
    return CollaborationRequest.objects.filter(
        influencer__user=user,
        brand=brand,
        status='completed'
    ).exists()


def already_reviewed_influencer(user, influencer):
    return Review.objects.filter(
        reviewer=user,
        influencer=influencer
    ).exists()


def already_reviewed_brand(user, brand):
    return Review.objects.filter(
        reviewer=user,
        brand=brand
    ).exists()


@login_required
def leave_review_influencer(request, pk):
    influencer = get_object_or_404(InfluencerProfile, pk=pk)

    # Must be a brand
    if request.user.role != 'brand':
        messages.error(request, 'Only brands can review creators.')
        return redirect('influencers:detail', pk=pk)

    # Must have completed collaboration
    if not has_completed_collab_with_influencer(request.user, influencer):
        messages.error(
            request,
            'You can only review a creator after completing a collaboration with them.'
        )
        return redirect('influencers:detail', pk=pk)

    # Already reviewed
    if already_reviewed_influencer(request.user, influencer):
        messages.warning(request, 'You have already reviewed this creator.')
        return redirect('influencers:detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.influencer = influencer
            review.save()
            # Update avg rating
            reviews = influencer.reviews.all()
            influencer.avg_rating = round(
                sum(r.rating for r in reviews) / reviews.count(), 2
            )
            influencer.total_reviews = reviews.count()
            influencer.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('influencers:detail', pk=influencer.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/leave_review.html', {
        'form': form,
        'target': influencer,
        'target_type': 'influencer',
        'target_name': influencer.user.get_full_name() or influencer.user.username,
    })


@login_required
def leave_review_brand(request, pk):
    brand = get_object_or_404(BrandProfile, pk=pk)

    # Must be an influencer
    if request.user.role != 'influencer':
        messages.error(request, 'Only creators can review brands.')
        return redirect('brands:detail', pk=pk)

    # Must have completed collaboration
    if not has_completed_collab_with_brand(request.user, brand):
        messages.error(
            request,
            'You can only review a brand after completing a collaboration with them.'
        )
        return redirect('brands:detail', pk=pk)

    # Already reviewed
    if already_reviewed_brand(request.user, brand):
        messages.warning(request, 'You have already reviewed this brand.')
        return redirect('brands:detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.brand = brand
            review.save()
            # Update avg rating
            reviews = brand.reviews.all()
            brand.avg_rating = round(
                sum(r.rating for r in reviews) / reviews.count(), 2
            )
            brand.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('brands:detail', pk=brand.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/leave_review.html', {
        'form': form,
        'target': brand,
        'target_type': 'brand',
        'target_name': brand.company_name,
    })