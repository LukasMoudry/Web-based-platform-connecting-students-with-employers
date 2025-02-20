from django.db import models
from django.contrib.auth.models import User

# Student and Employer profiles are linked one-to-one with the built-in User model.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

# Job postings created by employers.
class JobListing(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Applications submitted by students.
class Application(models.Model):
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.student.user.username} - {self.job_listing.title}"

# Simple messaging between users.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"
