import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from review.models import Ticket


# Inspired by https://techincent.com/how-to-delete-file-when-models-instance-is-delete-or-update-in-django/
@receiver(pre_save, sender=Ticket)
def delete_old_img(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


@receiver(post_delete, sender=Ticket)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass
