from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (('student', 'Student'), ('teacher', 'Teacher'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    attendance = models.FloatField(default=0.0)
    last_semester_marks = models.FloatField(default=0.0)
    grade = models.CharField(max_length=2, default='F')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)