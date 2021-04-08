from datetime import datetime, timezone

from team.models import UserActivity


def get_request_properties(request):
    """
    Provides the type of activity and should log or not
    :param request:
    :return: IsLoggable, Activity type
    """
    if '/api-auth/login/' == request.path:
        return {'loggable': True, 'activity': 'login'}
    else:
        return {'loggable': True, 'activity': 'activity'}


def log_user_activity(request, user):
    rq_properties = get_request_properties(request)
    if rq_properties['loggable']:
        last_activity = UserActivity.objects.all().filter(user=request.user).order_by('time').last()
        delta = 0
        now = datetime.now(timezone.utc)
        if last_activity:
            delta = (now - last_activity.time).seconds

        activity = UserActivity.objects.create(user=request.user, time=now,
                                               action=rq_properties['activity'], delta=delta)
        activity.save()
    pass
