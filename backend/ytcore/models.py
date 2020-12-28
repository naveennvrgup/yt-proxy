from django.db import models
from datetime import timedelta, timezone


class YTVideo(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    thumbnail_url=models.URLField()
    publish_time=models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.publish_time} >> {self.title}"