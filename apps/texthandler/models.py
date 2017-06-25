from django.db import models
import uuid

class UserProfile(models.Model):
    name = models.CharField(max_length=1000)
    identification_profile_id = models.CharField(max_length=1000)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Audio(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=1000)
    users = models.ManyToManyField(UserProfile, null=False)

    def __unicode__(self):
        return self.filename

    def __str__(self):
        return self.filename

class TextBlock(models.Model):
    sequence_number = models.IntegerField(default=0, null=False)
    audio = models.ForeignKey(Audio, null=False)
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    filename = models.CharField(max_length=1000)
    content = models.CharField(max_length=5000, blank = True, null=True)

    def __unicode__(self):
        return self.audio.filename + "-" + str(self.sequence_number)
    def __str__(self):
        return self.audio.filename + "-" + str(self.sequence_number)
