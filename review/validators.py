from django.core.exceptions import ValidationError
from django.conf import settings
from django.template.defaultfilters import filesizeformat


def validate_image_size(image):
    if image.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            "L'image doit faire moins de {}. Actuellement, l'image fait {}.".format(
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)
            )
        )
