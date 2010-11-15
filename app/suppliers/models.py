from django.db import models
from core.models import PersistentModel
from app.contacts.models import Contact
from django.core import urlresolvers

class Supplier(PersistentModel):
    name = models.CharField(max_length=200)
    contacts = models.ManyToManyField(Contact, related_name="suppliers")

    def __unicode__(self):
        return self.name

    def getViewUrl(self):
        return urlresolvers.reverse('app.suppliers.views.view', args=("%s" % self.id,))