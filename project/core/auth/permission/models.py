# -*- coding: utf-8 -*-
from core.cache import cachedecorator
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from core import Core

class Action(models.Model):
    name = models.CharField(max_length=40, unique=True)
    verb = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):

        cache_key = "get_action_by_name_%s" % name
        cached = cache.get(cache_key)

        if cached is not None:
            return cached

        act = Action.objects.get(name=name)
        cache.set(cache_key, act)
        return act

    @classmethod
    def get_list_by_names(cls, actions):

        if isinstance(actions, (list, set)):
            act = [Action.get_by_name(action) for action in actions]
        else:
            act = [Action.get_by_name(actions)]

        return act
    
class Role(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    actions = models.ManyToManyField(Action, related_name="role")

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def get_by_name(cls, name):
        cache_key = "get_role_by_name_%s" % name
        cached = cache.get(cache_key)

        if cached is not None:
            return cached

        act = Role.objects.get(name=name)
        cache.set(cache_key, act)
        return act

    @cachedecorator('get_actions')
    def get_actions(self):
        return list(self.actions.all())

    def grant_actions (self, actions):

        for p in Action.get_list_by_names(actions):
            self.actions.add(p)

        self.save()

        for perm in self.permissions.all():
            perm.invalidate_cache_for_user_and_members_of_groups()


class Permission(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="permissions")
    object_id = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('user.User', blank=True, null=True, related_name="permissions")
    group = models.ForeignKey('group.Group', blank=True, null=True, related_name='permissions')
    role = models.ForeignKey(Role, blank=True, null=True, related_name="permissions")
    deleted = models.BooleanField()
    actions = models.ManyToManyField(Action)

    negative = models.BooleanField()
    from_date = models.DateTimeField(null=True, blank=True)
    to_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        if self.user:
            return _("User") + ":" + " " + unicode(self.user)

        return _("Group") + ":" + " " + unicode(self.group)

    def invalidate_cache_for_user_and_members_of_groups(self):
        if self.user_id != 0 and self.user:
            self.user.invalidate_permission_tree()

        if self.group:
            self.group.invalidate_permission_tree_for_members()

        cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_actions"))

    @cachedecorator('get_actions')
    def get_actions(self):
        actions = []
        if self.actions:
            actions.extend(self.actions.all())
        if self.role:
            actions.extend(self.role.get_actions())

        return list(actions)

    def get_valid_actions(self):

        actions = self.get_actions()

        today = datetime.today()

        if not self.from_date:
            self.from_date = today - timedelta(days=1)
        if not self.to_date:
            self.to_date = today + timedelta(days=1)

        result = []
        if today > self.from_date and today < self.to_date:
            result = list(actions)

        return result

    def get_object(self):
        if not self.object_id:
            return "any"
        try:
            return self.content_type.get_object_for_this_type(id=self.object_id)
        except Exception, e:
            return "error, %s, %s" % (self.object_id, str(e))