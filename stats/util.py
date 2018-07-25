from django.db.models import F, Q


def db_bool(cond):
    if cond:
        return Q(pk=F('pk'))
    return ~Q(pk=F('pk'))
