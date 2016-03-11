from django.db import models
from phoneusers.models import PhoneUser


class SuperbaCDRManager(models.Manager):

    def valid(self):
        return self.filter(valid=True)

    def incoming(self):
        return self.filter(direction=SuperbaCDR.DIRECTION_INCOMING)

    def outgoing(self):
        return self.filter(direction=SuperbaCDR.DIRECTION_OUTGOING)



class SuperbaCDR(models.Model):
    """
    SuperbaCDR

    Mappa il cdr custom
    """

    CALL_ORDINARY = 0
    CALL_EXTRAORDINARY = 1
    CALL_SPECIAL = 2

    CALL_TYPES = (
        (CALL_ORDINARY, 'ordinaria'),
        (CALL_EXTRAORDINARY, 'strordinaria'),
        (CALL_SPECIAL, 'speciale'),
    )

    DIRECTION_INTERCOM = 0
    DIRECTION_OUTGOING = 1
    DIRECTION_INCOMING = 2

    DIRECTIONS = (
        (DIRECTION_INTERCOM, 'interna'),
        (DIRECTION_OUTGOING, 'uscente'),
        (DIRECTION_INCOMING, 'entrante'),
    )

    calldate = models.DateTimeField()
    src = models.CharField(max_length=80, default='')
    dst = models.CharField(max_length=80, default='')
    pincode = models.CharField(max_length=40, default='')
    calltype = models.IntegerField(choices=CALL_TYPES, default=CALL_ORDINARY)
    direction = models.IntegerField(choices=DIRECTIONS, default=DIRECTION_OUTGOING)
    duration = models.IntegerField(default=0)
    billsec = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    valid = models.BooleanField(default=True)
    uniqueid = models.CharField(max_length=32, default='')

    class Meta:
        db_table = 'superbacdr'


    def __unicode__(self):
        return "Chiamata da %s a %s del %s" % (self.src,
                                               self.dst,
                                               self.calldate)



    @staticmethod
    def get_cost(phoneuser):
        """Calcola il totale dei costi sostenuti"""
        try:
            total = SuperbaCDR.objects.filter(pincode=phoneuser.pincode).aggregate(total=models.Sum('price'))
            return total['total']
        except Exception as e:
            return None
