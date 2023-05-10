from django.utils.timezone import now
from django.core.exceptions import ValidationError


def validate_max_year(value):
    if value > now().year:
        raise ValidationError('год не может быть более текущего')
    return value
