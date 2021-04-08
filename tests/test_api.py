from django.contrib.auth.models import User, Group

from team.models import Team
from tests.test_setup import TestSetup


class TestPlayer(TestSetup):
    def test_user_can_create_player(self):
        self.group = Group.objects.create(name='player')
        player_user = {'username': 'player1',
                       'password': '123',
                       'email': 'pla@gmail.com',
                       'groups': [1]
                       }
        res_user = self.client.post(self.user_url, player_user)
        self.assertEqual(res_user.status_code, 201)
        self.team = Team.objects.create(name='Team1', coach_id=1)

        player = {'name': 'playernae',
                  'user': 2,
                  'team': 1,
                  'height': 150
                  }

        res_player = self.client.post(self.player_url, player)
        self.assertEqual(res_player.status_code, 403)
