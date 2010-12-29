from django.db import models
from app.contacts.models import Contact
from core.models import PersistentModel
from django.core import urlresolvers
from core.models import User

class Customer(PersistentModel):
    cid = models.IntegerField("Kundenr")
    full_name = models.CharField("Fullt navn", max_length=80)
    email = models.EmailField("Epostadresse", max_length=80)
    address = models.CharField("Adresse", max_length=80, blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    zip = models.CharField("Postnr", max_length=4, blank=True)
    city = models.CharField("By", max_length=20, blank=True)
    website = models.CharField("Hjemmeside", max_length=150, blank=True, null=True)
    alternative_address = models.CharField("Alternativ adresse", max_length=20, blank=True)
    owner = models.ForeignKey(User, blank=True, related_name="UsersContacts");
    contacts = models.ManyToManyField(Contact, blank=True, related_name="customers", verbose_name="Kontakter")

    def __unicode__(self):
        return self.full_name

    def getViewUrl(self):
        return urlresolvers.reverse('app.customers.views.view', args=("%s" % self.id,))