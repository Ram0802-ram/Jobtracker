from django.shortcuts import render, redirect
from .forms import JobApplicationForm
from .models import JobApplication
from django.contrib.auth.decorators import login_required

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'job/add_job.html', {'form': form})


@login_required
def dashboard(request):
    query = request.GET.get('q')
    jobs = JobApplication.objects.filter(user=request.user)

    if query:
        jobs = jobs.filter(company_name__icontains=query)

    context = {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'interviews': jobs.filter(status='Interview').count(),
        'selected': jobs.filter(status='Selected').count(),
        'rejected': jobs.filter(status='Rejected').count(),
    }

    return render(request, 'job/dashboard.html', context)

from django.shortcuts import get_object_or_404

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobApplicationForm(instance=job)

    return render(request, 'job/add_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    job.delete()
    return redirect('dashboard')
