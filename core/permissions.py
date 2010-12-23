from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from core.managers import PersistentManager
from . import Core
from core.user import User, Membership

"""
Actions("ADD","EDIT","VIEW"..)
"""
class Action(models.Model):
    action = models.CharField(max_length=40)
    verb = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.action

"""
ROLES ("Leader", "Member"..)
"""
class Role(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    actions = models.ManyToManyField(Action, related_name="role")

    def __unicode__(self):
        return unicode(self.content_type)


class Permission(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="permissions")
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, blank=True, null=True, related_name="permissions")
    membership = models.ForeignKey(Membership, blank=True, null=True, related_name='permissions')
    role = models.ForeignKey(Role, blank=True, null=True, related_name="permissions")
    deleted = models.BooleanField()

    def __unicode__(self):
        return unicode(self.content_type)

    def get_object(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

