# -*- coding: utf-8 -*-
from django.db import models
from core.models import PersistentModel

class Email(models.Model):
    from_email = models.TextField(default="")
    from_name = models.CharField(max_length=230, default="")
    to = models.TextField(default="")
    cc = models.TextField(default="")
    bcc = models.TextField(default="")
    tag = models.TextField(default="")
    message_id = models.TextField(default="")
    mailbox_hash = models.TextField(default="")
    reply_to = models.TextField(default="")
    html_body = models.TextField(default="")
    text_body = models.TextField(default="")

    subject  = models.TextField()

    def __unicode__(self):
        return "Email from %s, subject: %s" % (self.from_email, self.subject)

class EmailHeader(models.Model):
    email = models.ForeignKey(Email, related_name="headers")
    name = models.CharField(max_length=230)
    value = models.CharField(max_length=230)

    def __unicode__(self):
        return self.name

class EmailAttachment(models.Model):
    email = models.ForeignKey(Email, related_name="attachments")
    content_length = models.CharField(max_length=230)
    name = models.CharField(max_length=230)
    content_type = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return "Attachment: %s" % self.name