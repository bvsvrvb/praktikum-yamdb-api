from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_max_year(value):
    if value > now().year:
        raise ValidationError('год не может быть более текущего')
    return value
