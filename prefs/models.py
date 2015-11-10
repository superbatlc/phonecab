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

    def save(self, user, *args, **kwargs):
        """Override funzione save per loggare azione"""
        try:
            super(Pref, self).save(*args, **kwargs)
            audit = Audit()
            audit.user = user
            audit.what = "L'utente %s ha modificato la preferenza %s impostandola al valore %s" \
                % (user.username, self.key, str(self.value))
            audit.save()
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
    visible = models.BooleanField(default=True)

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

    @staticmethod
    def check_prefix_existance(phonenumber):
        """Restituisce 1 se il prefisso del numero passato compare nel db. 0 altrimenti"""
        from django.db import connection
        cursor = connection.cursor()

        # recuperiamo la tariffa corrispondente alla espressione regolare
        # che matcha con l'ordine minore
        query = """SELECT COUNT(*) AS n FROM %s
                        WHERE '%s' REGEXP reg_exp""" % (Fare._meta.db_table, phonenumber)
        print query
        cursor.execute(query)

        existance = cursor.fetchone()
        if existance:
            return str(existance[0])
        return "0"

    def save(self, user, *args, **kwargs):
        """Override della funzione save per impostare correttamente le espressioni regolari
        e loggare azione"""
        self._create_regexp_from_prefix_list()

        try:
            super(Fare, self).save(*args, **kwargs)
            audit = Audit()
            audit.user = user
            detail = "Scatto: %s - Tariffa: %s - Lista Prefissi: %s" % (
                self.connection_charge, self.fee_per_second, self.prefix_list)
            audit.what = "Modifica direttrice %s : %s" % (self.direction, detail)
            audit.save()
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))

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
