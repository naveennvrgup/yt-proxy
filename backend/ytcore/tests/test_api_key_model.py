from django.test import TestCase
from ytcore.models import ApiKey
from decouple import config
from cryptography.fernet import Fernet


class ApiKeyModelTestCase(TestCase):
    def setUp(self):
        self.sample_key = 'i am the secret key'


    def test_encryption_and_decryption(self):
        # to protect the api key it must be encrypted while
        # stored in the db

        key_obj = ApiKey.objects.create(key=self.sample_key)

        self.assertNotEqual(key_obj.key,self.sample_key)

        # testing decryption
        f = Fernet(config('SECRET_KEY').encode())
        actual=f.decrypt(key_obj.key.encode()).decode()

        self.assertEqual(actual, self.sample_key)


    def test_avoid_double_encryption_during_updation(self):
        # the key value should not be encryption more than one 
        # time due to updating the db record

        key_creation = ApiKey.objects.create(key=self.sample_key)
        expected = key_creation.key

        key_creation.quota = 20
        key_creation.save()

        key_after_update = ApiKey.objects.get(id=key_creation.id)
        actual = key_after_update.key

        self.assertEqual(actual, expected)