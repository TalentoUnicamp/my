from rest_framework import permissions


class IsReadyOnlyRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsPostRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "POST"


class IsGetRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "GET"


class IsPutPatchRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "PUT" or request.method == "PATCH"


class IsDeleteRequest(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "DELETE"


class OwnsObject(permissions.BasePermission):

    def has_permission(self, request, view):
        """Tries to check if an object belongs to the user
        ownership_field: The field in the object that corresponds to the user
        user_relation: The relation from user that owns the object
        """
        obj = view.get_object()
        ownership_field = view.ownership_field
        user_relation = view.user_relation
        obj_field = obj
        for field in ownership_field.split('.'):
            obj_field = getattr(obj, field)
        u_rel = request
        for field in user_relation.split('.'):
            u_rel = getattr(u_rel, field)
        return obj_field == u_rel
