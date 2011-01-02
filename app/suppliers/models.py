from django.db import models
from core import Core
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

    def save(self, *args, **kwargs):

        new = False
        if not self.id:
            new = True

        super(Supplier, self).save()

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)