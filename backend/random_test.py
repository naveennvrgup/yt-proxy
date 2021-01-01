from ytcore.tasks import *
from ytcore.models import *

fetch_from_yt()

# sample=[]
# for x in YTVideo.objects.all():
#     sample.append([x.title,x.description,x.thumbnail_url,x.publish_time.isoformat("T")[:-6] + "Z"])
# print(sample)