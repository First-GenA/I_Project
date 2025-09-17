from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField


# Create your models here.
class UserFeedback(models.Model):
    """
    Records user feedback from the website
    """
    name = models.CharField(max_length=20)
    message = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    Profile information for the user
    """
    u_name = models.CharField(max_length=20, blank=True, null=True)  # default set to login username util changed
    u_address = models.CharField(max_length=200, blank=True, null=True)
    u_phone = models.CharField(default=00 - 0000 - 0000, blank=True, null=True)
    u_avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BankInfo(models.Model):
    """
    Holds bank records
    """
    b_name = models.CharField(max_length=20)
    b_balance = models.FloatField(default=0.0)
    b_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bank')

    def __str__(self) -> CharField:
        return self.b_name


class Transactions(models.Model):
    """
    Records transaction history
    """
    t_amount = models.FloatField(default=0.0)
    t_type = models.CharField(max_length=13)
    t_bank = models.ForeignKey(BankInfo, on_delete=models.CASCADE)
    t_owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    t_creation = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.t_owner.u_name


class Items(models.Model):
    """
    Records items
    """
    i_name = models.CharField(max_length=30, null=False)
    i_description = models.TextField(null=False)
    i_price = models.FloatField(default=0.0)
    i_total_quantity = models.IntegerField()
    # i_owner = models.ForeignKey()
