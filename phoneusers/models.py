import datetime
from django.db import models
from audits.models import Audit


class PhoneUser(models.Model):
    """
    Phoneuser

    Modella la scheda anagrafica.
    """

    ITALIAN = 'it'
    ENGLISH = 'en'
    FRENCH = 'fr'
    GERMAN = 'de'
    SPANISH = 'es'
    ARABIC = 'ar'

    LANGUAGES = (
        (ITALIAN, 'Italiano'),
        (ENGLISH, 'Inglese'),
        (FRENCH, 'Francese'),
        (GERMAN, 'Tedesco'),
        (SPANISH, 'Spagnolo'),
        (ARABIC, 'Arabo'),
    )

    first_name = models.CharField(max_length=35, verbose_name="nome")
    last_name = models.CharField(max_length=50, verbose_name="cognome")
    pincode = models.CharField(max_length=10, verbose_name="pin")
    serial_no = models.CharField(
        max_length=24, verbose_name="matricola", default='')
    listening_enabled = models.BooleanField(
        verbose_name="ascolto", default=False)
    recording_enabled = models.BooleanField(
        verbose_name="registrazione", default=False)
    enabled = models.BooleanField(verbose_name="stato", default=True)
    balance = models.DecimalField(
        verbose_name="credito residuo",
        default=0,
        max_digits=7,
        decimal_places=4)
    language = models.CharField(
        max_length=4, verbose_name="lingua", choices=LANGUAGES, default='it')
    additional_calls = models.IntegerField(
        verbose_name="chiamate supplementari", default=0)
    vipaccount = models.BooleanField(
        verbose_name="senza restizioni", default=False)
    four_bis_limited = models.BooleanField(
        verbose_name="4bis limitato", default=False)

    def get_full_name(self):
        return "%s %s" % (self.last_name, self.first_name)

    @staticmethod
    def get_from_pincode(pincode):
        items = PhoneUser.objects.filter(pincode=pincode)
        if items:
            return items[0]
        return None

    @staticmethod
    def get_from_serial_no(serial_no):
        items = PhoneUser.objects.filter(serial_no=serial_no)
        if items:
            return items[0]
        return None

    def __unicode__(self):
        return "%s %s (matricola %s codice %s)" % (self.last_name,
            self.first_name,
            self.serial_no,
            self.pincode)


class Whitelist(models.Model):

    """
    Whitelist

    Modella i numeri che il phoneuser puo chiamare
    """

    ORDINARY_KIND = 0           # free
    SPECIAL_KIND = 1

    KINDS = (
        (ORDINARY_KIND, 'Ordinaria'),
        (SPECIAL_KIND, 'Primo ingresso'),
    )

    phoneuser = models.ForeignKey(PhoneUser)
    label = models.CharField(max_length=255, verbose_name="etichetta")
    phonenumber = models.CharField(max_length=40, verbose_name="telefono")
    duration = models.IntegerField(verbose_name="durata massima", default=10)
    kind = models.IntegerField(
        verbose_name="tipologia",
        choices=KINDS,
        default=ORDINARY_KIND)
    lawyer = models.BooleanField(
        verbose_name='avvocato',
        default=False)
    extraordinary = models.BooleanField(
        verbose_name='straordinaria',
        default=False)
    # definisce se un cellulare debba essere trattato come tale o come fisso
    real_mobile = models.BooleanField(
        verbose_name='cellulare',
        default=False)
    enabled = models.BooleanField(verbose_name="stato", default=False)

    def __unicode__(self):
        return "Numero %s (%s) relativo a %s" % (self.phonenumber,
            self.label,
            self.phoneuser,)


class Credit(models.Model):

    """
    Classe Credit

    Modella le ricariche effettuate dal phoneuser
    """
    phoneuser = models.ForeignKey(PhoneUser)
    recharge = models.DecimalField(
        verbose_name="ricarica", default=0, max_digits=5, decimal_places=2)
    recharge_date = models.DateTimeField(default=datetime.datetime.now)
    reason = models.CharField(max_length=255)

    @staticmethod
    def get_total(phoneuser):
        """Restituisce il totale delle ricariche effettuate"""
        total = Credit.objects.filter(phoneuser=phoneuser).aggregate(total=models.Sum('recharge'))
        return total['total']
