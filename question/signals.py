from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Problem, dispatch_uid="Create-MD-File")
def createMarkdown(sender, instance, created, **kwargs):
    if created:
        print("yayyyyyyyyyyyyy")
        # CODE TO MAKE A MARKDOWN FILE USING QUESTION.MAKRDOWN
