from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

from .models import *


@receiver(post_save, sender=Problem, dispatch_uid="Create-MD-File")
def createMarkdown(sender, instance, created, **kwargs):
    if created:
        print("yayyyyyyyyyyyyy")
        # CODE TO MAKE A MARKDOWN FILE USING QUESTION.MAKRDOWN


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)