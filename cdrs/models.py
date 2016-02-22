from django.db import models
from phoneusers.models import PhoneUser


class DetailManager(models.Manager):

    """Custom Manager per recuperare solo le chiamate"""

    def get_queryset(self):
        return super(DetailManager, self).get_queryset().filter(
            lastapp='Dial')


class Detail(models.Model):

    """
    Detail

    Modella la tabella automaticamente riempita da Asterisk
    """
    calldate = models.DateTimeField()
    clid = models.CharField(max_length=80, default='')
    src = models.CharField(max_length=80, default='')
    dst = models.CharField(max_length=80, default='')
    dcontext = models.CharField(max_length=80, default='')
    channel = models.CharField(max_length=80, default='')
    dstchannel = models.CharField(max_length=80, default='')
    lastapp = models.CharField(max_length=80, default='')
    lastdata = models.CharField(max_length=80, default='')
    duration = models.IntegerField(default=0)
    billsec = models.IntegerField(default=0)
    disposition = models.CharField(max_length=45, default='')
    amaflags = models.IntegerField(default=0)
    # rappresenta il pincode anagrafica
    accountcode = models.CharField(max_length=20, default='')
    userfield = models.CharField(max_length=255, default='')
    uniqueid = models.CharField(max_length=32, default='')
    linkedid = models.CharField(max_length=32, default='')
    sequence = models.CharField(max_length=32, default='')
    peeraccount = models.CharField(max_length=32, default='')
    price = models.DecimalField(default=-1.00, max_digits=7, decimal_places=4)
    custom_src = models.CharField(max_length=80, default='')
    custom_dst = models.CharField(max_length=80, default='')
    custom_calltype = models.IntegerField(default=0)
    custom_valid = models.BooleanField(default=True)

    objects = DetailManager()
    all_objects = models.Manager()

    @staticmethod
    def get_cost(phoneuser_id):
        """Calcola il totale dei costi sostenuti"""
        try:
            phoneuser = PhoneUser.objects.get(pk=phoneuser_id)
            total = Detail.objects.filter(accountcode=phoneuser.pincode).aggregate(total=models.Sum('price'))
            return total['total']
        except Exception as e:
            print format(e)
            pass # TODO gestire errore


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



    @staticmethod
    def get_cost(phoneuser):
        """Calcola il totale dei costi sostenuti"""
        try:
            total = SuperbaCDR.objects.filter(pincode=phoneuser.pincode).aggregate(total=models.Sum('price'))
            return total['total']
        except Exception as e:
            return None
