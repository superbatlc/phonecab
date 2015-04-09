from django.db import models
from django.conf import settings
import datetime


class Record(models.Model):

    """
    Record

    Modella i file audio delle chiamate
    """
    calldate = models.DateTimeField(datetime.datetime.now())
    pincode = models.CharField(max_length=10, default='')
    uniqueid = models.CharField(max_length=32, default='')
    filename = models.CharField(max_length=255, default='')

    def delete_all(self, delete_file=True):
        """Override della funzione delete per cancellare fisicamente il file"""
        if delete_file:
            try:
                self._remove_file_from_filesystem()
            except:
                pass
        self.delete()

    def _remove_file_from_filesystem(self):
        """Rimuove il file indicato dal path"""
        import os
        path = "%s%s" % (settings.RECORDS_ROOT, self.filename)
        os.remove(path)
