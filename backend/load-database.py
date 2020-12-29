from ytcore.models import *
from decouple import config
from dateutil.parser import parse
from django.contrib.auth.models import User


print(''.center(75,'*'))
print("loading database with sample data".center(75,'*'))
print(''.center(75,'*'))


su = User(username='admin')
su.set_password('admin')
su.is_superuser = True
su.is_staff = True
su.save()

print("superuser created:")
print("username: admin")
print("password: admin")



ApiKey.objects.all().delete()
ApiKey.objects.create(key=config('GGL_API_KEY'))
ApiKey.objects.create(key=config('GGL_API_KEY'))
ApiKey.objects.create(key=config('GGL_API_KEY'))
ApiKey.objects.create(key=config('GGL_API_KEY'))
print(ApiKey.objects.count()," keys loaded")


sample_data = [
    [
        'Hindi News Live: बुधवार दोपहर 2 बजे होगी किसान-सरकार वार्ता I Top 100 I Nonstop 100 I Dec 29, 2020', 
        'Aaj Ki Taaja Khabar: किसानों का आंदोलन 34वें दिन भी जारी है. बुधवार को दोपहर 2 बजे 7वें दौर की वार्ता होगी. इस बातचीत से ...',
        'https://i.ytimg.com/vi/FPRNAdsmIxU/hqdefault.jpg',
        '2020-12-29T02:09:02Z'
    ],[
        'Morning News With Mallanna 29-12-2020 || TeenmarMallanna #QNews || #QGroupMedia',
        'MLC ELECTION voter enrollment: http://ceotserms1.telangana.gov.in/MLC/form18.aspx ▻For More Videos On Q News HD :https://shorturl.at/cpwKZ #GHMC ...',
        'https://i.ytimg.com/vi/VNJa2PJ6AZc/hqdefault_live.jpg',
        '2020-12-29T01:53:09Z'
    ],[
        'Super 100: Non-Stop Superfast | December 29,2020 | IndiaTV News',
        'Catch all the latest updates of the day at breakneck speed on Super 100: Non-Stop Superfast bulletin. For more videos,visit https://www.indiatvnews.com/video ...',
        'https://i.ytimg.com/vi/euIR1JSuwvY/hqdefault.jpg',
        '2020-12-29T01:39:33Z'
    ],
    [
        'WATCH LIVE: CBC Vancouver News at 6 for December 28  —  Activist sentenced &amp; public washroom access',
        "Watch CBC Vancouver News at 6 with host Tanya Fletcher for the latest on the most important news stories happening across B.C. She's joined by meteorologist ...",
        'https://i.ytimg.com/vi/UK7AUjarlf4/hqdefault_live.jpg', 
        '2020-12-29T01:33:11Z'
    ],
]

YTVideo.objects.all().delete()
for x in sample_data:
    YTVideo.objects.create(
        title=x[0],
        description=x[1],
        thumbnail_url=x[2],
        publish_time=parse(x[3]),
    )
print(YTVideo.objects.count()," sample vids loaded")


print(''.center(75,'*'))
print("provision complete".center(75,'*'))
print(''.center(75,'*'))