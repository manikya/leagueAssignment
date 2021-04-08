from django.contrib.auth.models import User
from django.db import models

from django.db.models import Sum, Q, Avg


class Team(models.Model):
    name = models.CharField('name', max_length=128)
    coach = models.ForeignKey(User, related_name='coach', on_delete=models.CASCADE)

    @property
    def team_average(self):
        team_score = Score.objects.filter(player__team=self.id).aggregate(Sum('score'))
        sum_of_score = team_score['score__sum']
        number_of_games = len(Game.objects.filter(Q(team1=self.id) | Q(team2=self.id)))
        if number_of_games == 0:
            return 0

        return float(sum_of_score) / number_of_games

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField('name', max_length=128)
    user = models.ForeignKey(User, related_name='player_user', on_delete=models.CASCADE)
    height = models.IntegerField('height')
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)

    @property
    def player_average(self):
        agr = Score.objects.filter(player_id=self.id).aggregate(Avg('score'))
        avg = agr['score__avg']
        if avg is None:
            return 0
        else:
            return avg

    @property
    def number_of_games(self):
        # if participated there is a record. if not scored then score=0
        return len(Score.objects.filter(player_id=self.id))

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField('name', max_length=128)
    round = models.IntegerField('round')
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Score(models.Model):
    game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE)
    score = models.IntegerField('score')


class UserActivity(models.Model):
    user = models.ForeignKey(User, related_name='actor', on_delete=models.CASCADE)
    action = models.CharField('action', max_length=20)
    time = models.DateTimeField()
    delta = models.IntegerField('delta')


class UserActivityStat(models.Model):
    @property
    def username(self):
        return User.objects.get(self.id).username

    @property
    def last_login(self):
        return User.objects.get(self.id).last_login

    @property
    def active_time(self):
        user = User.objects.get(self.id)
        # get records having inactive time less than 60 seconds and sum it up
        sum_val = UserActivity.objects.all().filter(user=user, delta__lte=60).aggregate(Sum('delta'))
        return sum_val['delta__sum']
