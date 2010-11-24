from django.db import models

from core.models import PersistentModel
from django.core import urlresolvers

class Announcement(PersistentModel):
    title = models.CharField("Overskrift", max_length=80)
    text = models.TextField("Tekst")
    attachment = models.FileField(upload_to="uploads/announcements/", verbose_name="Vedlegg", null=True, blank=True)

    def __unicode__(self):
        return self.title

    def getViewUrl(self):
        return urlresolvers.reverse('app.announcements.views.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.announcements.views.edit', args=("%s" % self.id,))