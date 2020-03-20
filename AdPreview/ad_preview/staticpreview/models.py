from django.db import models

__PREVIEW_LENGTH__ = 10000
__DEFAULT_CHAR_FIELD_LENGTH__ = 50


class StaticAdPreview(models.Model):
    id = models.AutoField(primary_key=True)
    preview = models.CharField(max_length=__PREVIEW_LENGTH__, blank=True)
    facebook_preview_type = models.CharField(max_length=__DEFAULT_CHAR_FIELD_LENGTH__, blank=True)

    def __str__(self):
        return "Preview: {0}... of Preview type: {1}".format(self.preview[:50], self.facebook_preview_type)
