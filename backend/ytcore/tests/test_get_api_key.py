from django.test import TestCase
from ytcore.models import ApiKey
from ytcore.tasks import get_api_key
from decouple import config
from cryptography.fernet import Fernet
from datetime import date, timedelta


class FetchAPIKeyTestCase(TestCase):
    def setUp(self):
        self.sample_key='sample_key'
    

    def test_get_key_with_quota_unused(self):
        expected = ApiKey.objects.create(key=self.sample_key)
        actual = get_api_key()    
        
        self.assertEqual(expected.id, actual.id)


    def test_decrypt_key_with_quota_unused(self):
        ApiKey.objects.create(key=self.sample_key)
        expected = self.sample_key
        
        key_obj = get_api_key()    
        f = Fernet(config('SECRET_KEY').encode())
        actual = f.decrypt(key_obj.key.encode()).decode()
        
        self.assertEqual(expected, actual)


    def test_get_key_among_keys_with_exhausted_quota(self):
        # Two keys with exhausted quota are created 
        # one key with unused quota is created
        # right behaviour is to obtain the third key

        ApiKey.objects.create(key=self.sample_key, quota=1, used=1)
        ApiKey.objects.create(key=self.sample_key, quota=1, used=1)
        ApiKey.objects.create(key=self.sample_key, quota=1, used=0)

        key_obj = get_api_key()
        self.assertIsNotNone(key_obj)


    def test_exhausted_quota(self):
        ApiKey.objects.create(key=self.sample_key, quota=1, used=1)
        ApiKey.objects.create(key=self.sample_key, quota=1, used=1)

        with self.assertRaises(RuntimeError):
            get_api_key()


    def test_should_update_date_in_key(self):
        # when came across a key with full quota used the day before
        # the get function should update the quota usage to nil
        # and update date to today

        key_obj = ApiKey.objects.create(
            key=self.sample_key, 
            quota=1, 
            used=1, 
            last_used_date=date.today()-timedelta(days=1))
        
        actual = get_api_key()

        self.assertIsNotNone(actual)
        self.assertEqual(actual.last_used_date, date.today())
