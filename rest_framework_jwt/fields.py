# Standard Library
from django.db.models import EmailField
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageUploadPath(object):
    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            'image',
            str(instance.id),
        )

class LowerEmailField(EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value
