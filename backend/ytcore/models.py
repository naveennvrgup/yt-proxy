from django.db import models
from datetime import timedelta, timezone, date
from django.db.models.signals import pre_save
from decouple import config
from cryptography.fernet import Fernet


# This stores the details fetched from youtube
class YTVideo(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    thumbnail_url=models.URLField()
    publish_time=models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.publish_time} >> {self.title}"


# This stores API_KEY and quota per day of the API_KEY
# On every use of api we increment the usage record of that key.
# also last used date is recorded with every use
# if the last used date is not the current date then the usage record is reset
class ApiKey(models.Model):
    key=models.CharField(max_length=200)
    quota=models.IntegerField(default=10)
    used=models.IntegerField(default=0)
    last_used_date=models.DateField(default=date.today, editable=True)

    def __str__(self):
        return f"{self.id} >> {self.used}/{self.quota} in {self.last_used_date}"


# API_KEY should not be stored naked in the database
# so the key is encrypted before storing in the database
# this signal runs while a new api key is registed in the database
def api_key_presave_handler(sender, instance, **kwargs):
    if instance._state.adding: # encrypt the key only once (that is while it is created)
        secret_key = config('SECRET_KEY')
        f = Fernet(secret_key)
        instance.key=f.encrypt(instance.key.encode()).decode()

pre_save.connect(api_key_presave_handler, sender=ApiKey)