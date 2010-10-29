from django.db import models

# Create your models here.
from core.models import PersistentModel
from app.contacts.models import Contact

class Supplier(PersistentModel):

    name = models.CharField(max_length=200)
    contacts = models.ManyToManyField(Contact, related_name="suppliers")


    def __unicode__(self):
        return self.name