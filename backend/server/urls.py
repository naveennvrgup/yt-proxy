from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

# swagger docs
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="YT-PROXY [We are a backup for youtube's news videos]",
      default_version='v1',
      description="""
      ## Docs
         Hello there! The docs are hosted at [https://github.com/naveennvrgup/yt-proxy](https://github.com/naveennvrgup/yt-proxy)
      """,
   ),
   public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/',schema_view.with_ui('swagger',cache_timeout=0), name = 'schema-swagger-ui'),
    path('api/', include('ytcore.urls')),
    re_path('', TemplateView.as_view(template_name="index.html")),
]