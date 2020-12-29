from celery import shared_task
import requests
from decouple import config
from ytcore.models import YTVideo, ApiKey
from dateutil.parser import parse
from datetime import date
from cryptography.fernet import Fernet
import traceback


# 1. fetch all api keys
# 2. reset usage value if last used date is not today
# 3. return the first api key with usage quota left
# 4. if no quota left throw a err
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

    raise RuntimeError("API Keys Quota Overflow!")


# scheduled at server.celery
@shared_task
def fetch_from_yt():
    key_obj=get_api_key() # fetch api key
    f = Fernet(config('SECRET_KEY').encode()) # decrypt api key
    API_KEY=f.decrypt(key_obj.key.encode()).decode()

    # build request url
    query_string='news'
    published_after='2020-12-26T16:51:48Z'
    r = requests.get(f'https://www.googleapis.com/youtube/v3/search?q={query_string}&part=snippet&key={API_KEY}&maxResults=40&publishedAfter={published_after}&type=video&order=date')

    # check for favourable output
    if r.status_code!=200:
        raise RuntimeError("Youtube says: API Quota Overflow!")
    
    # parse the videos list
    videos = r.json()['items']

    # record api key usage
    key_obj.used+=1
    key_obj.save()

    # get last video in the DB reversely chronologically
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
        
        # check if this video is already present in DB 
        # this is done with timestamp of last video
        # since the video frequency is not on a per second basis
        # this method provides sufficient results
        # O(1) operation hence scalable
        if last_video:
            if last_video.publish_time < new_video.publish_time:
                new_videos.append(new_video)
        else:
            new_videos.append(new_video)
    
    print(new_videos)
    # using bulk create for efficiency
    YTVideo.objects.bulk_create(new_videos)

    

