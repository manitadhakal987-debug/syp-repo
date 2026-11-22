from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    CITY_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Lalitpur', 'Lalitpur'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Pokhara', 'Pokhara'),
        ('Chitwan', 'Chitwan'),
        ('Butwal', 'Butwal'),
        ('Biratnagar', 'Biratnagar'),
        ('Dharan', 'Dharan'),
        ('Hetauda', 'Hetauda'),
        ('Nepalgunj', 'Nepalgunj'),
        ('Other', 'Other Nepal Location'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, help_text="e.g. 98XXXXXXXX")
    address_line = models.CharField(max_length=255, blank=True, help_text="Street, Tole or Landmark")
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Kathmandu')
    district = models.CharField(max_length=100, default='Kathmandu')
    bio = models.TextField(blank=True, help_text="Tell us about your curl journey!")
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        if self.user.first_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
