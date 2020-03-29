from __future__ import annotations

from app.models.guests import Guest
from tortoise import fields

from .base import CustomTortoiseBase, TimestampMixin


class Feature(TimestampMixin, CustomTortoiseBase):
    id = fields.UUIDField(pk=True, read_only=True)
    title = fields.CharField(max_length=100, unique=True)
    slug = fields.CharField(index=True, required=True, unique=True, max_length=50)
    turn_duration = fields.IntField(required=True)
    guests = fields.ReverseRelation[Guest]

    class Meta:
        table = "features"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.id)} name='{self.title}'>"

    def __str__(self):
        return self.__repr__()

    class PydanticMeta:
        exclude = (
            "created_at",
            "updated_at",
        )
