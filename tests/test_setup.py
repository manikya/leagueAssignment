import base64

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestSetup(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='superuser', password='123')
        self.api_authentication()

        self.score_url = 'http://127.0.0.1:8000/score/'
        self.user_url = 'http://127.0.0.1:8000/users/'
        self.player_url = 'http://127.0.0.1:8000/player/'

        return super().setUp()

    def api_authentication(self):
        credentials = base64.b64encode(b'superuser:123').decode("ascii")
        self.client.credentials(HTTP_AUTHORIZATION="Basic " + credentials)

    def tearDown(self):
        return super().tearDown()
