from django.db.models import Window, F, Avg
from django.db.models.functions import PercentRank

from team.permission import is_in_group


def filter_query_with_visible_players(queryset, user):
    """
    Filter the user by request senders permission level (Data driven permission)
    :param queryset:
    :param user:
    :return:
    """
    if is_in_group(user, 'coach'):
        return queryset.filter(team__coach=user.id)

    elif is_in_group(user, 'admin'):
        return queryset


def filter_query_with_percentile(percentile, queryset):
    """
    Calculate players percentile and filter to given value
    :param percentile:
    :param queryset:
    :return:
    """
    # filter on percentile when user requested
    if percentile:
        queryset = queryset.annotate(Avg('player__score')).annotate(
            percentile=Window(expression=PercentRank(), order_by=F('player__score__avg').asc(), ))

        # queryset does not support filtering after window operation
        final_data = []
        for elm in queryset:
            if elm.percentile >= float(percentile):
                final_data.append(elm)
        queryset = final_data

    return queryset
