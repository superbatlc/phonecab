from django.db import models
from django.contrib.auth.models import User


class Acl(models.Model):

    """
    Classe ACL

    Modella i permessi di accesso alle varie funzioni
    definite nella tupla FUNCTION
    """

    FUNCTION_ACCOUNT = 0
    FUNCTION_WHITELIST = 1
    FUNCTION_CREDIT = 2
    FUNCTION_CDR = 3
    FUNCTION_RECORD = 4

    FUNCTION = (
        (FUNCTION_ACCOUNT, 'Anagrafica'),
        (FUNCTION_WHITELIST, 'Whitelist'),
        (FUNCTION_CREDIT, 'Ricarica'),
        (FUNCTION_CDR, 'Dettaglio'),
        (FUNCTION_RECORD, 'Registrazione'),
    )

    PERMISSION_NONE = 0
    PERMISSION_READING = 1
    PERMISSION_WRITING = 3

    PERMISSION = (
        (PERMISSION_NONE, ('Nessuno')),
        (PERMISSION_READING, ('Lettura')),
        (PERMISSION_WRITING, ('Scrittura')),
    )

    user = models.ForeignKey(User)
    function = models.CharField(max_length=1, choices=FUNCTION, blank=False)
    permission = models.CharField(
        max_length=1, choices=PERMISSION, blank=False)

    @staticmethod
    def get_permission_for_function(user_id, function):
        """Recupera il privilegio utente per la funzione passata. Zero se non presente"""
        try:
            obj = Acl.objects.get(user__id=user_id, function=function)
            return int(obj.permission)
        except Acl.DoesNotExist:
            return 0

    @staticmethod
    def get_permissions_for_user(user_id, is_admin=False):
        """Restituisce un dizionario dei privilegi utente per tutte le funzioni"""
        if is_admin:
            permission = {
                'priv_anagrafica': Acl.PERMISSION_WRITING,
                'priv_whitelist': Acl.PERMISSION_WRITING,
                'priv_credit': Acl.PERMISSION_WRITING,
                'priv_cdr': Acl.PERMISSION_READING,
                'priv_record': Acl.PERMISSION_READING
            }
        else:
            permission = {
                'priv_anagrafica': Acl.get_permission_for_function(
                    user_id, Acl.FUNCTION_ACCOUNT), 'priv_whitelist': Acl.get_permission_for_function(
                    user_id, Acl.FUNCTION_WHITELIST), 'priv_credit': Acl.get_permission_for_function(
                    user_id, Acl.FUNCTION_CREDIT), 'priv_cdr': Acl.get_permission_for_function(
                    user_id, Acl.FUNCTION_CDR), 'priv_record': Acl.get_permission_for_function(
                        user_id, Acl.FUNCTION_RECORD), }

        return permission
