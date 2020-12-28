from django.db import models
from datetime import timedelta, timezone, date


class YTVideo(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    thumbnail_url=models.URLField()
    publish_time=models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.publish_time} >> {self.title}"


class ApiKey(models.Model):
    key=models.CharField(max_length=100)
    quota=models.IntegerField(default=10)
    used=models.IntegerField(default=0)
    last_used_date=models.DateField(default=date.today, editable=True)

    def __str__(self):
        return f"{self.id} >> {self.used}/{self.quota} in {self.last_used_date}"