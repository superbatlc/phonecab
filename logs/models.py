from django.db import models

class Log(models.Model):
    """
    Log

    Show logs from Diaplan actions to the user
    """

    INFO = 0
    WARNING = 1
    ERROR = 2

    LEVELS = (
        (INFO, "info"),
        (WARNING, "warning"),
        (ERROR, "error"),
    )

    USER = 0
    WHITELIST = 1
    CREDIT = 2

    KINDS = (
        (USER, "utente"),
        (WHITELIST, "numero autorizzato"),
        (CREDIT, "credito"),
    )

    when = models.DateTimeField()
    what = models.TextField()
    level = models.IntegerField(choices=LEVELS, default=0)
    kind = models.IntegerField(choices=KINDS, default=0)
