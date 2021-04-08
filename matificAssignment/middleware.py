from datetime import datetime

from django.contrib.auth.models import AnonymousUser

from matificAssignment.user_activity_service import log_user_activity
from team.models import UserActivity


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_anonymous:
            log_user_activity(request, request.user)

        return response
