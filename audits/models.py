import datetime
from django.db import models
from django.contrib.auth.models import User


class Audit(models.Model):

    """
    Audit

    Consente di registrare tutte le azioni che vengono compiute
    """

    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)
    what = models.TextField()
    params = models.CharField(max_length=255)

    def __unicode__(self):
        return "[%s - %s] %s" % (self.when, self.user.username, self.what)

    def get_action(self, visualized_by_user=False):
        pass

    def log(self, user, what, params=None):
        """Shortcut to create a new audit entry"""
        self.user = user
        self.what = what
        self.when = datetime.datetime.now()
        if params:
            self.params = params

        self.save()
