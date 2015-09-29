import datetime
from django.db import models

from phoneusers.models import PhoneUser, Whitelist, Credit
from cdrs.models import Detail
from records.models import Record


class ArchivedPhoneUser(models.Model):
    """
    ArchivedPhoneUser

    This class stores the information about an archived phoneuser
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

    phoneuser = None

    first_name = models.CharField(max_length=35, verbose_name="nome")
    last_name = models.CharField(max_length=50, verbose_name="cognome")
    pincode = models.CharField(max_length=10, verbose_name="pin")
    serial_no = models.CharField(
        max_length=24, verbose_name="matricola", default='')
    listening_enabled = models.BooleanField(
        verbose_name="ascolto", default=False)
    recording_enabled = models.BooleanField(
        verbose_name="registrazione", default=False)
    language = models.CharField(
        max_length=4, verbose_name="lingua", choices=LANGUAGES)
    vipaccount = models.BooleanField(
        verbose_name="senza restizioni", default=False)
    balance = models.DecimalField(
        verbose_name="credito residuo",
        default=0,
        max_digits=5,
        decimal_places=2)
    four_bis_limited = models.BooleanField(
        verbose_name="4bis limitato", default=False)
    archived_date = models.DateTimeField(default=datetime.datetime.now)

    """
    def __init__(self, *args, **kwargs):
        self.phoneuser = kwargs.pop('phoneuser')
        super(ArchivedPhoneUser, self).__init__(*args, **kwargs)
    """
    
    def copy(self):
        """Copys values between phoneuser and archivephoneuser"""
        self.first_name = self.phoneuser.first_name
        self.last_name = self.phoneuser.last_name
        self.pincode = self.phoneuser.pincode
        self.serial_no = self.phoneuser.serial_no
        self.listening_enabled = self.phoneuser.listening_enabled
        self.recording_enabled = self.phoneuser.recording_enabled
        self.language = self.phoneuser.language
        self.vipaccount = self.phoneuser.vipaccount
        self.four_bis_limited = self.phoneuser.four_bis_limited
        self.balance = self.phoneuser.balance

    def delete_related(self):
        self.phoneuser.delete()

    def archive(self, delete=True):
        """Archives all phoneuser information"""
        # 1. archive phoneuser
        self._archive_phoneuser()
        # 2. archive all phoneusers's whitelists
        self._archive_whitelist(delete)
        # 3. archive all phoneusers's credits info
        self._archive_credit(delete)
        # 4. archive all cdr details
        self._archive_detail(delete)
        # 5. archive all records
        self._archive_record(delete)
        # 6 delete original phoneuser
        self.delete_related()

    def _archive_phoneuser(self):
        """
        Copys and saves ArchivedPhoneUser instance
        """
        self.copy()
        self.save()

    def _archive_whitelist(self, delete=False):
        """
        Archives all the whitelists and if required
        deletes them from the phoneusers_whitelist table
        """
        whitelists = Whitelist.objects.filter(phoneuser=self.phoneuser)
        for whitelist in whitelists:
            archived_whitelist = ArchivedWhitelist()
            archived_whitelist.archived_phoneuser = self
            archived_whitelist.copy(whitelist)
            archived_whitelist.save()
            if delete:
                whitelist.delete()

    def _archive_credit(self, delete=False):
        """
        Archives all the credits and if required
        deletes them from the phoneusers_credit table
        """
        credits = Credit.objects.filter(phoneuser=self.phoneuser)
        for credit in credits:
            archived_credit = ArchivedCredit()
            archived_credit.archived_phoneuser = self
            archived_credit.copy(credit)
            archived_credit.save()
            if delete:
                credit.delete()

    def _archive_detail(self, delete_details=False):
        """
        Archives all the cdr details and if required
        deletes them from the cdrs_detail table
        """
        details = Detail.objects.filter(accountcode=self.phoneuser.pincode)
        print details
        for detail in details:
            archived_detail = ArchivedDetail()
            archived_detail.archived_phoneuser = self
            archived_detail.copy(detail)
            archived_detail.save()

            if delete_details:
                detail.delete()

    def _archive_record(self, delete_details=False):
        """
        Archives all the records and if required
        deletes them from the records table
        """
        records = Record.objects.filter(pincode=self.phoneuser.pincode)

        for record in records:
            archived_record = ArchivedRecord()
            archived_record.archived_phoneuser = self
            archived_record.copy(record)
            archived_record.save()

            if delete_details:
                record.delete_all()


class ArchivedWhitelist(models.Model):
    """
    ArchivedWhitelist

    This class stores the whitelists of an archived phoneuser
    """

    FIRST_FREQUENCY = 0           # free
    LAWYER_FREQUENCY = 1          # free
    ORDINARY_FREQUENCY = 2        # 1 per week
    ORDINARY_4BIS_FREQUENCY = 3   # 2 per month not in the same week

    CALL_FREQUENCY = (
        (FIRST_FREQUENCY, 'Primo Ingresso'),
        (LAWYER_FREQUENCY, 'Avvocato'),
        (ORDINARY_FREQUENCY, 'Ordinaria'),
        (ORDINARY_4BIS_FREQUENCY, 'Ordinaria 4bis limitato')
    )

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
    label = models.CharField(max_length=255, verbose_name="etichetta")
    phonenumber = models.CharField(max_length=40, verbose_name="telefono")
    duration = models.IntegerField(verbose_name="durata massima")
    frequency = models.IntegerField(
        verbose_name="frequenza",
        choices=CALL_FREQUENCY)
    extraordinary = models.BooleanField(
        verbose_name='straordinaria', default=False)
    real_mobile = models.BooleanField(
        verbose_name='cellulare', default=False)

    def copy(self, whitelist):
        self.label = whitelist.label
        self.phonenumber = whitelist.phonenumber
        self.duration = whitelist.duration
        self.frequency = whitelist.frequency
        self.extraordinary = whitelist.extraordinary
        self.real_mobile = whitelist.real_mobile


class ArchivedCredit(models.Model):
    """
    ArchivedCredit

    This class stores the credits of an archived phoneuser
    """

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
    recharge = models.DecimalField(
        verbose_name="ricarica", default=0, max_digits=5, decimal_places=2)
    recharge_date = models.DateTimeField()

    def copy(self, credit):
        self.recharge = credit.recharge
        self.recharge_date = credit.recharge_date


class ArchivedDetail(models.Model):
    """
    ArchivedDetail

    This class stores the cdr details of an archived phoneuser
    """

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
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
    price = models.DecimalField(default=0, max_digits=7, decimal_places=4)
    custom_src = models.CharField(max_length=80, default='')
    custom_dst = models.CharField(max_length=80, default='')
    custom_calltype = models.IntegerField(default=0)

    def copy(self, detail):
        self.calldate = detail.calldate
        self.clid = detail.clid
        self.src = detail.src
        self.dst = detail.dst
        self.dcontext = detail.dcontext
        self.channel = detail.channel
        self.dstchannel = detail.dstchannel
        self.lastapp = detail.lastapp
        self.lastdata = detail.lastdata
        self.duration = detail.duration
        self.billsec = detail.billsec
        self.disposition = detail.disposition
        self.amaflags = detail.amaflags
        self.accountcode = detail.accountcode
        self.userfield = detail.userfield
        self.uniqueid = detail.uniqueid
        self.linkedid = detail.linkedid
        self.sequence = detail.sequence
        self.peeraccount = detail.peeraccount
        self.price = detail.price
        self.custom_src = detail.custom_src
        self.custom_dst = detail.custom_dst
        self.custom_calltype = detail.custom_calltype


class ArchivedRecord(models.Model):
    """
    ArchivedRecord

    This class stores the records of an archived phoneuser
    """

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
    calldate = models.DateTimeField()
    pincode = models.CharField(max_length=10, default='')
    uniqueid = models.CharField(max_length=32, default='')
    filename = models.CharField(max_length=255, default='')

    def copy(self, record):
        self.calldate = record.calldate
        self.pincode = record.pincode
        self.uniqueid = record.uniqueid
        self.filename = record.filename
