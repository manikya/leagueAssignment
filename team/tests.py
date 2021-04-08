from django.contrib.auth.models import Group, User
from django.test import TestCase

from team.models import Team, Player
from team.service import filter_query_with_visible_players


class CoachPlayerTestCase(TestCase):
    def setUp(self):
        self.group_coach = Group.objects.create(name='coach')
        self.group_coach.save()

        self.user_coach = User.objects.create_user(username='coach1', email='coach2@gmail.com', password='123')
        self.user_coach.groups.add(self.group_coach)
        self.user_coach.save()

        self.player1_user = User.objects.create_user(username='player1', email='player1@gmail.com', password='123')
        self.player1_user.save()
        self.player2_user = User.objects.create_user(username='player2', email='player2@gmail.com', password='123')
        self.player2_user.save()

        self.team1 = Team.objects.create(name='team1', coach=self.user_coach)
        self.team1.save()

        self.player1 = Player.objects.create(name='Player 1', height=150, team=self.team1, user=self.player1_user)
        self.player1.save()

    def test_coach_can_only_see_players_in_team(self):
        players = filter_query_with_visible_players(Player.objects.all(), self.user_coach)
        self.assertEqual(len(players), 1)
