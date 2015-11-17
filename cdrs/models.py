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
            pass #TODO gestire errore


class RealTimeCall(models.Model):

    """
    RealTimeCall

    Modella i dati nella tabella delle chiamate realtime
    """
    pincode = models.CharField(max_length=10, default='')
    src = models.CharField(max_length=80, default='')
    dst = models.CharField(max_length=80, default='')
    calldate = models.IntegerField()
    max_duration = models.IntegerField(default=0)
    balance = models.FloatField(default=0)
    connection_charge = models.FloatField(default=0)
    fee_per_second = models.FloatField(default=0)
    channel = models.CharField(max_length=80, default='')
