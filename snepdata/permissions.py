from rest_framework import permissions
from snepdata.models import Token

class BearerTokenPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            return False
        if token.startswith('Bearer'):
            try:
                Token.objects.get(token=token.split(' ')[-1])
                return True
            except Token.DoesNotExist:
                return False