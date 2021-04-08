from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from team.models import Team, Player, Game, Score, UserActivity
from team.permission import IsAdminUser, IsCoachUser, IsCoachOrAdminUser
from team.serializer import UserSerializer, GroupSerializer, TeamSerializer, PlayerSerializer, GameSerializer, \
    ScoreSerializer, UserActivitySerializer, UserActivityStatSerializer
from team.service import filter_query_with_visible_players, filter_query_with_percentile


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsCoachOrAdminUser]

    def get_queryset(self):
        queryset = Player.objects.all()
        percentile = self.request.query_params.get('percentile')
        # filter player for coach
        queryset = filter_query_with_visible_players(queryset, self.request.user)
        # filter player with score percentile
        queryset = filter_query_with_percentile(percentile, queryset)

        return queryset


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class ScoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows game score to be viewed or edited.
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]


class UserActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user activity to be viewed or edited.
    """
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get']


class UserActivityStatViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserActivityStatSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get']
