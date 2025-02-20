from django.contrib import admin
from .models import StudentProfile, EmployerProfile, JobListing, Application, Message

admin.site.register(StudentProfile)
admin.site.register(EmployerProfile)
admin.site.register(JobListing)
admin.site.register(Application)
admin.site.register(Message)
