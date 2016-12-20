import datetime
from django.db import models

from phoneusers.models import PhoneUser, Whitelist, Credit
from cdrs.models import SuperbaCDR
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
    additional_calls = models.IntegerField(
        verbose_name="chiamate supplementari", default=0)
    additional_due_date = models.DateTimeField(
        verbose_name="scadenza chiamate supplementari", null=True)
    vipaccount = models.BooleanField(
        verbose_name="senza restizioni", default=False)
    balance = models.DecimalField(
        verbose_name="credito residuo",
        default=0,
        max_digits=7,
        decimal_places=4)
    four_bis_limited = models.BooleanField(
        verbose_name="4bis limitato", default=False)
    archived_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "%s %s (matricola %s codice %s)" % (self.last_name,
            self.first_name,
            self.serial_no,
            self.pincode)

    def get_full_name(self):
        return "%s %s" % (self.last_name, self.first_name)

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
        self.additional_calls = self.phoneuser.additional_calls
        self.additional_due_date = self.phoneuser.additional_due_date
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
        details = SuperbaCDR.objects.filter(pincode=self.phoneuser.pincode)
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

    ORDINARY_KIND = 0           # free
    SPECIAL_KIND = 1

    KINDS = (
        (ORDINARY_KIND, 'Ordinaria'),
        (SPECIAL_KIND, 'Primo ingresso'),
    )

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
    label = models.CharField(max_length=255, verbose_name="etichetta")
    phonenumber = models.CharField(max_length=40, verbose_name="telefono")
    duration = models.IntegerField(verbose_name="durata massima")
    kind = models.IntegerField(
        verbose_name="tipologia",
        choices=KINDS,
        default=ORDINARY_KIND)
    lawyer = models.BooleanField(
        verbose_name='avvocato',
        default=False)
    extraordinary = models.BooleanField(
        verbose_name='straordinaria', default=False)
    real_mobile = models.BooleanField(
        verbose_name='cellulare', default=False)

    def copy(self, whitelist):
        self.label = whitelist.label
        self.phonenumber = whitelist.phonenumber
        self.duration = whitelist.duration
        self.kind = whitelist.kind
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
    reason = models.CharField(max_length=255, default='')

    def copy(self, credit):
        self.recharge = credit.recharge
        self.recharge_date = credit.recharge_date
        self.reason = credit.reason

    @staticmethod
    def get_total(archived_phoneuser):
        """Restituisce il totale delle ricariche effettuate"""
        total = ArchivedCredit.objects.filter(
            archived_phoneuser=archived_phoneuser).aggregate(total=models.Sum('recharge'))
        return total['total']


class ArchivedDetail(models.Model):
    """
    ArchivedDetail

    This class stores the cdr details of an archived phoneuser
    """

    archived_phoneuser = models.ForeignKey(ArchivedPhoneUser)
    calldate = models.DateTimeField()
    src = models.CharField(max_length=80, default='')
    dst = models.CharField(max_length=80, default='')
    calltype = models.IntegerField(default=0)
    direction = models.IntegerField(default=1)
    lawyer = models.BooleanField(default=False)
    duration = models.IntegerField(default=0)
    billsec = models.IntegerField(default=0)
    # rappresenta il pincode anagrafica
    pincode = models.CharField(max_length=40, default='')
    uniqueid = models.CharField(max_length=32, default='')
    price = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    valid = models.BooleanField(default=True)


    def copy(self, detail):
        self.calldate = detail.calldate
        self.src = detail.src
        self.dst = detail.dst
        self.duration = detail.duration
        self.billsec = detail.billsec
        self.pincode = detail.pincode
        self.uniqueid = detail.uniqueid
        self.price = detail.price
        self.direction = detail.direction
        self.calltype = detail.calltype
        self.lawyer = detail.lawyer
        self.valid = detail.valid

    @staticmethod
    def get_cost(archived_phoneuser):
        """Calcola il totale dei costi sostenuti"""

        total = ArchivedDetail.objects.filter(
            archived_phoneuser_id=archived_phoneuser).aggregate(total=models.Sum('price'))
        cost = total['total']
        if cost:
            return cost
        return None


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
