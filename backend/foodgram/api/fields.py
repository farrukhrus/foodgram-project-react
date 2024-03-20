import base64
import webcolors
import uuid

from rest_framework import serializers
from django.core.files.base import ContentFile
from recipe.models import Subscription


class NameToColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('У цвета нет названия')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_name = str(uuid.uuid4())
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=file_name + '.' + file_extension
            )

        return super().to_internal_value(data)


def is_sub(user, subscriber):
    if user.is_authenticated:
        return Subscription.objects.filter(
            user=user, subscriber=subscriber
        ).exists()
    return False
