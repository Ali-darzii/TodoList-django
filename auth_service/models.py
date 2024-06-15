from django.db import models
from django.contrib.auth.models import User
from utils.utils import get_client_ip
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in, user_login_failed


class UserLogins(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_logins')
    no_logins = models.PositiveIntegerField(default=0)
    failed_attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email + '_logins'

    class Meta:
        verbose_name = 'User Login'
        verbose_name_plural = 'User Logins'
        db_table = 'UserLogins_DB'


class UserIP(models.Model):
    user_logins = models.ForeignKey(UserLogins, on_delete=models.CASCADE, related_name='ips')
    ip = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_logins.user.email) + '_ip'

    class Meta:
        verbose_name = 'User IPs'
        verbose_name_plural = 'User IP'
        db_table = 'UserIP_DB'


class UserDevice(models.Model):
    user_logins = models.ForeignKey(UserLogins, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=100)
    is_phone = models.BooleanField(default=False)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)

    @classmethod
    def get_user_device(cls, request, user):
        device_name = request.user_agent.device.family
        is_phone = request.user_agent.is_mobile
        browser = request.user_agent.browser.family
        os = request.user_agent.os.family
        return cls(device_name=device_name, is_phone=is_phone, browser=browser, os=os, user_logins=user.user_logins)

    def __str__(self):
        return str(self.user_logins.user.email) + '_device'

    class Meta:
        verbose_name = 'User Devices'
        verbose_name_plural = 'User Device'
        db_table = 'UserDevice_DB'


@receiver(signal=post_save, sender=User)
def create_user_logins(sender, instance, created, **kwargs):
    """ after User created, Create User Login """
    if created:
        user_logins = UserLogins(user=instance)
        user_logins.save()


@receiver(signal=user_logged_in)
def create_user_ip(sender, user, request, **kwargs):
    """ after user logged in, create user ip"""
    ip = UserIP(ip=get_client_ip(request), userlogin=user.user_logins)
    user.user_logins.no_logins += 1
    user.save()
    ip.save()


@receiver(signal=user_logged_in)
def create_user_device(sender, user, request, **kwargs):
    """ after user logged in, create user device"""
    user_device = UserDevice().get_user_device(request, user)
    user_device.save()


@receiver(signal=user_logged_in)
def login_failed(sender, request, user, **kwargs):
    """ after user login failed """
    user.user_logins.failed_attempts += 1
    ip = UserIP(ip=get_client_ip(), userlogin=user.user_logins, failed=True)
    ip.save()
    user.save()
