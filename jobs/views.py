from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

from .models import JobListing, Application, Message, StudentProfile, EmployerProfile
from .forms import ApplicationForm, MessageForm, StudentRegistrationForm, EmployerRegistrationForm

def home(request):
    return render(request, 'jobs/home.html')

def job_list(request):
    jobs = JobListing.objects.all().order_by('-posted_date')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(JobListing, pk=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            try:
                student_profile = request.user.studentprofile
            except StudentProfile.DoesNotExist:
                messages.error(request, "Only students can apply for jobs.")
                return redirect('job_detail', job_id=job_id)
            application.student = student_profile
            application.job_listing = job
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/job_detail.html', {'job': job, 'form': form})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user).order_by('-sent_date')
    return render(request, 'jobs/inbox.html', {'messages': messages_received})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'jobs/send_message.html', {'form': form, 'recipient': recipient})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'jobs/register_student.html', {'form': form})

def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.pop('company_name')
            user = form.save()
            EmployerProfile.objects.create(user=user, company_name=company_name)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'jobs/register_employer.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'jobs/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')
