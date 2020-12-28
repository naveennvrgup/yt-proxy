from celery import shared_task
import requests
from decouple import config
from ytcore.models import YTVideo
from dateutil.parser import parse

@shared_task
def helloworld():
    print("celery hello world")
    return "celery hello world"


@shared_task
def fetch_from_yt():
    API_KEY=config('GGL_API_KEY')
    query_string='news'
    published_after='2020-12-26T16:51:48Z'

    r = requests.get(f'https://www.googleapis.com/youtube/v3/search?q={query_string}&part=snippet&key={API_KEY}&maxResults=20&publishedAfter={published_after}&type=video&order=date')
    videos = r.json()['items']
    
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

    

