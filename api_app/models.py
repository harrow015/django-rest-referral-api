from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager
from .utils import generate_referral_token




class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    referral_points = models.IntegerField(default=0) 
    referral_code = models.CharField(default=generate_referral_token(), max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)
        return super().save(*args, **kwargs)


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referr")
    referred_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.email
