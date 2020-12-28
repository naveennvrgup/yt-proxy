from celery import shared_task
import requests
from decouple import config
from ytcore.models import YTVideo, ApiKey
from dateutil.parser import parse
from datetime import date


def get_api_key():
    keys = ApiKey.objects.all()
    today = date.today()

    for key in keys:
        if key.last_used_date < today:
            key.last_used_date=today
            key.used=0
            key.save()

    for key in keys:
        if key.used < key.quota:
            return key

    raise RuntimeError("API Quota Overflow")


@shared_task
def fetch_from_yt():
    API_KEY=get_api_key()
    query_string='news'
    published_after='2020-12-26T16:51:48Z'

    r = requests.get(f'https://www.googleapis.com/youtube/v3/search?q={query_string}&part=snippet&key={API_KEY.key}&maxResults=20&publishedAfter={published_after}&type=video&order=date')
    videos = r.json()['items']

    API_KEY.used+=1
    API_KEY.save()

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

    

