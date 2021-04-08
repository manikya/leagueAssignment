from django.contrib.auth.models import Group
from rest_framework import permissions


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    return is_in_group_user_id(user.id, group_name)


def is_in_group_user_id(user_id, group_name):
    """
    Takes a user id and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user_id).exists()
    except Group.DoesNotExist:
        return None


def has_group_permission(user, required_groups):
    return any([is_in_group(user, group_name) for group_name in required_groups])


class IsCoachOrAdminUser(permissions.BasePermission):
    required_groups = ['admin', 'coach']

    def has_permission(self, request, view):
        group_permission = has_group_permission(request.user, self.required_groups)
        return request.user and group_permission


class IsCoachUser(permissions.BasePermission):
    # group_name for coach
    required_groups = ['coach']

    def has_permission(self, request, view):
        group_permission = has_group_permission(request.user, self.required_groups)
        return request.user and group_permission


class IsAdminUser(permissions.BasePermission):
    # group_name for admin
    required_groups = ['admin']

    def has_permission(self, request, view):
        group_permission = has_group_permission(request.user, self.required_groups)
        return request.user and group_permission
