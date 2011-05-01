from app.tickets.models import Ticket
from core.models import PersistentModel
from django.db import models
from django.utils.translation import ugettext as _

class TicketClient(PersistentModel):
    email = models.EmailField()
    password = models.CharField(_('password'), max_length=128, blank=True)
    tickets = models.ManyToManyField(Ticket, related_name="clients")


    def save(self, **kwargs):
        if not self.id:
            self.password = self.generate_password()
        super(TicketClient, self).save()


    @staticmethod
    def generate_password():
        import string
        import random

        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = [a for a in string.ascii_lowercase if a not in vowels]
        ret = ''
        slen = 8
        for i in range(slen):
            if not i % 2:
                randid = random.randint(0, 20) #number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0, 4) #number of vowels
                ret += vowels[randid]

        return ret




