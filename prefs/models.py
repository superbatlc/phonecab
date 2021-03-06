from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from audits.models import Audit


class Pref(models.Model):

    """
    Pref

    Modella un sistema di preferenze chiave-valore
    """
    key = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

    def __unicode__(self):
        return "key: %s - value: %s" % (self.key, self.value)

    def save(self, user, *args, **kwargs):
        """Override funzione save per loggare azione"""
        try:
            super(Pref, self).save(*args, **kwargs)
            audit = Audit()
            what = "L'utente %s ha modificato la preferenza %s impostandola al valore %s" \
                % (user.username, self.key, str(self.value))
            audit.log(user=user, what=what)
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))

    @staticmethod
    def get(key):
        """Returns the value corresponding to key"""
        try:
            pref = Pref.objects.get(key=key)
            return pref.value
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    @staticmethod
    def header():
        """Return the value of the header pref for printing"""
        return Pref.get("header")


class Fare(models.Model):

    """
    Fare

    Modella le tariffe in funzione delle direttrici
    """
    direction = models.CharField(max_length=80, verbose_name="Direttrice")
    prefix_list = models.TextField(verbose_name="Lista prefissi")
    connection_charge = models.FloatField(verbose_name="Scatto alla risposta")
    fee_per_second = models.FloatField(verbose_name="Tariffa al secondo")
    reg_exp = models.TextField(verbose_name="Espressione regolare")
    ordering = models.IntegerField(verbose_name="Ordinamento")
    icon = models.CharField(max_length=50, default="zmdi zmdi-home")
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return "direction: %s" % self.direction

    @staticmethod
    def get_call_cost(phonenumber, duration):
        """Restituisce il costo della chiamata sulla base del numero chiamato e della durata"""
        from django.db import connection
        cursor = connection.cursor()

        # recuperiamo la tariffa corrispondente alla espressione regolare
        # che matcha con l'ordine minore
        query = """SELECT connection_charge, fee_per_second
                FROM %s WHERE '%s' REGEXP reg_exp
                ORDER BY ordering LIMIT 1""" % (Fare._meta.db_table, phonenumber)
        cursor.execute(query)

        fare = cursor.fetchone()

        return (float(fare[0]) + float(fare[1]) * duration) / 100  # eurocent


    def save(self, user, *args, **kwargs):
        """Override della funzione save per impostare correttamente le espressioni regolari
        e loggare azione"""
        self._create_regexp_from_prefix_list()

        try:
            super(Fare, self).save(*args, **kwargs)
            audit = Audit()
            detail = "Scatto: %s - Tariffa: %s - Lista Prefissi: %s" % (
                self.connection_charge, self.fee_per_second, self.prefix_list)
            what = "Modifica direttrice %s : %s" % (self.direction, detail)
            audit.log(user=user, what=what)
        except Exception as e:
            print '%s (%s)' % (e.message, type(e)) # TODO gestire errore

    def _create_regexp_from_prefix_list(self):
        """Crea le espressioni regolari necessarie per associare una tariffa
        al numero chiamato a partire da una serie di prefissi separati da virgole"""
        if self.prefix_list != "":
            prefixes = self.prefix_list.split(",")
            result = []
            for prefix in prefixes:
                if prefix != "":
                    result.append("^%s[0-9]+" % prefix.strip())

            self.reg_exp = "|".join(result)


class Extension(models.Model):
    """
    Definisce i nomi che si vogliono assegnare agli inetrni
    """

    extension = models.CharField(max_length=5, default='')
    name = models.CharField(max_length=20, default='')

    def __unicode__(self):
        return "extension: %s - name: %s" % (self.extension, self.name)

    @staticmethod
    def get_extension_name(extension):
        """Restituisce il nome estensione o solo estensione"""
        try:
            ext = Extension.objects.get(extension=extension)
            name = "%s (%s)" % (ext.name, extension)
        except:
            name = extension
        return name





