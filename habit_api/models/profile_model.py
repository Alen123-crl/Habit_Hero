from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    pro_pic = models.ImageField(
    upload_to='profiles/',
    blank=True,
    null=True,
    default='defaults/default.png'  
)

    def __str__(self):
        return f"{self.user.email} Profile"
    
    def save(self, *args, **kwargs):
        if not self.pro_pic:
            self.pro_pic = 'defaults/default.png'
        super().save(*args, **kwargs)