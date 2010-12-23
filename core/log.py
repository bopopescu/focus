# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from core.user import User
from core.models import Company

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name="notifications")
    text = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    company = models.ForeignKey(Company, related_name="notifications", null=True)
    creator = models.ForeignKey(User, related_name="createdNotifications", null=True)

    #If true, add note to daily-mail updates
    sendEmail = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

    def getObject(self, *args, **kwargs):
        o = ContentType.objects.get(model=self.content_type)
        k = o.get_object_for_this_type(id=self.object_id)
        return k

    def save(self, *args, **kwargs):
        self.date = datetime.now()
        #self.company = get_current_company()

        if 'user' in kwargs:
            self.creator = kwargs['user']
        else:
            self.creator = Core.current_user()

        super(Notification, self).save()

class Log(models.Model):
    date = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="logs", null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    message = models.TextField()
    company = models.ForeignKey(Company, related_name="logs", null=True)
    action = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        s = "%s, %s, %s:" % (self.date, (self.creator), self.content_type)
        return s


    def getObject(self, *args, **kwargs):
        o = ContentType.objects.get(model=self.content_type)
        k = o.get_object_for_this_type(id=self.object_id)
        return k

    def save(self, *args, **kwargs):
        self.date = datetime.now()

        if 'user' in kwargs:
            self.creator = kwargs['user']
        else:
            self.creator = Core.current_user()

        #self.company = self.creator.get_profile().company

        super(Log, self).save()