import datetime
from django.db import models
from django.contrib.auth.models import User


class Audit(models.Model):

    """
    Audit

    Consente di registrare tutte le azioni che vengono compiute
    """

    user = models.ForeignKey(User)
    when = models.DateTimeField(default=datetime.datetime.now())
    what = models.TextField()
    params = models.CharField(max_length=255)

    # class Meta:

    def get_action(self, visualized_by_user=False):
        pass
