from django.db import models
import uuid

class UserProfile(models.Model):
    name = models.CharField(max_length=1000)
    identification_profile_id = models.CharField(max_length=1000)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __unicode__(self):
        return self.name

class Audio(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=1000)
    users = models.ManyToManyField(UserProfile, null=False)

    def __unicode__(self):
        return self.uuid

class TextBlock(models.Model):
    sequence_number = models.IntegerField(default=0, null=False)
    audio = models.ForeignKey(Audio, null=False)
    user = models.ForeignKey(UserProfile, null=False)

    def __unicode__(self):
        return self.audio + str(self.sequence_number)

