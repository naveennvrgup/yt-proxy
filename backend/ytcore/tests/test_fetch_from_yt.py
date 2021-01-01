from django.test import TestCase
from unittest.mock import patch, Mock
from ytcore.models import ApiKey, YTVideo
from ytcore.tasks import fetch_from_yt
from decouple import config
import requests
from cryptography.fernet import Fernet


class FetchYTDataTestCase(TestCase):
    def setUp(self):
        self.sample_key='sample_key'
        self.sample_key_obj = ApiKey.objects.create(key='sample_key')

        self.sample_response = {"items": [
        {
            "snippet": {
                "title": "Solskjaer&#39;s 40 Million Swoop? Van De Beek Loan? Man Utd Transfer News",
                "description": "The United Stand are on Flick - join our group https://flick.group/theunitedstand. Man Utd are set to back Solskjaer this transfer window and could Van De Beek ...",
                "thumbnails": {"high": {"url": "https://i.ytimg.com/vi/EtGbxTn7NMs/hqdefault_live.jpg",
                    }},"publishTime": "2021-01-01T10:00:28Z"}
        },
        {
            "snippet": {
                "title": "Zee Top 50: अब तक की 50 बड़ी ख़बरें | Top News Today | Breaking News | Hindi News | Latest News",
                "description": "In this section, you will find the top news stories of the day. Segment News 50 is a part of Zee News important news bulletins in which we cover all the important ...",
                "thumbnails": { "high": { "url":"https://i.ytimg.com/vi/_Nss1ShBZ1U/hqdefault.jpg",
                }},"publishTime": "2021-01-01T09:51:03Z"
            }
        }]}



    @patch('ytcore.tasks.get_api_key')
    @patch('ytcore.tasks.requests.get')
    def test_increment_key_usage(self, mock_get, mock_get_api_key):
        # the api key usage infomation should be updated 
        # in the db after every api call

        mock_response = Mock()
        mock_response.json.return_value=self.sample_response
        mock_response.status_code = 200
        
        mock_get.return_value = mock_response
        mock_get_api_key.return_value = self.sample_key_obj 

        actual = fetch_from_yt()
        
        self.assertEqual(ApiKey.objects.get(id=self.sample_key_obj.id).used,1)
        self.assertEqual(YTVideo.objects.count(),2)


    @patch('ytcore.tasks.get_api_key')
    @patch('ytcore.tasks.requests.get')
    def test_duplicates_avoidance(self, mock_get, mock_get_api_key):
        # while polling the fetch operation duplicates records of video being 
        # created should be avoided

        old_video = self.sample_response['items'][1]['snippet']
        YTVideo.objects.create(
            title=old_video['title'],
            description=old_video['description'],
            thumbnail_url=old_video['thumbnails']['high']['url'],
            publish_time=old_video['publishTime'],
        )

        mock_response = Mock()
        mock_response.json.return_value=self.sample_response
        mock_response.status_code = 200
        
        mock_get.return_value = mock_response
        mock_get_api_key.return_value = self.sample_key_obj 

        actual = fetch_from_yt()

        self.assertEqual(YTVideo.objects.count(),2)
