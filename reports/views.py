from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report
from .forms import ReportForm
from accounts.models import User

@login_required
def file_report(request, user_id):
    reported_user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.save()
            messages.success(request, 'Report submitted. We will review it shortly.')
            return redirect('landing')
    else:
        form = ReportForm()
    return render(request, 'reports/file_report.html', {'form': form, 'reported_user': reported_user})