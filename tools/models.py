from django.db import models


class Activation(models.Model):
    """
    Activation Class

    Handle entries to activate and disactivate the system
    """

    activation_time = models.TimeField(null=False)
    disactivation_time = models.TimeField(null=False)

    def check_for_clash(self,):
        """
        Check for clashes between the provided period and the existing ones

        Return False if a clash is founded
        """
        pass

    def _set_cron_activation_time(self,):
        return "%s %s * * * /etc/asterisk/giorno.sh" % (self.activation_time.minute,
                                                        self.activation_time.hour)

    def _set_cron_deactivation_time(self,):
        return "%s %s * * * /etc/asterisk/notte.sh" % (self.deactivation_time.minute,
                                                       self.deactivation_time.hour)

    def change_cron(self,):
        pass