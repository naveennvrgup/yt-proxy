from celery import shared_task
import requests
from decouple import config
from ytcore.models import YTVideo, ApiKey
from dateutil.parser import parse
from datetime import date
from cryptography.fernet import Fernet


def get_api_key():
    keys = ApiKey.objects.all()
    today = date.today()

    for key_obj in keys:
        if key_obj.last_used_date < today:
            key_obj.last_used_date=today
            key_obj.used=0
            key_obj.save()

    for key_obj in keys:
        if key_obj.used < key_obj.quota:
            return key_obj

    raise RuntimeError("API Quota Overflow")



@shared_task
def fetch_from_yt():
    key_obj=get_api_key()
    f = Fernet(config('SECRET_KEY').encode())
    API_KEY=f.decrypt(key_obj.key.encode()).decode()

    query_string='news'
    published_after='2020-12-26T16:51:48Z'
    r = requests.get(f'https://www.googleapis.com/youtube/v3/search?q={query_string}&part=snippet&key={API_KEY}&maxResults=20&publishedAfter={published_after}&type=video&order=date')
    videos = r.json()['items']

    key_obj.used+=1
    key_obj.save()

    last_video = YTVideo.objects.order_by('-publish_time').first()
    
    new_videos = []
    for video in videos:
        snippet=video['snippet']
        
        new_video = YTVideo(
            title=snippet['title'],
            description=snippet['description'],
            thumbnail_url=snippet['thumbnails']['high']['url'],
            publish_time=parse(snippet['publishTime']),
        )
        
        if last_video:
            if last_video.publish_time < new_video.publish_time:
                new_videos.append(new_video)
        else:
            new_videos.append(new_video)

    print(new_videos)
    YTVideo.objects.bulk_create(new_videos)

    

