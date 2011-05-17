# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from datetime import datetime, timedelta

class Action(models.Model):
    name = models.CharField(max_length=40)
    verb = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    actions = models.ManyToManyField(Action, related_name="role")

    def __unicode__(self):
        return unicode(self.name)

    def grant_actions (self, actions):
        if(isinstance(actions, str)):
            act = Action.objects.filter(name=actions)
        else:
            act = Action.objects.filter(name__in=actions)

        for p in act:
            self.actions.add(p)

        self.save()

        cache.clear()


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



    def get_actions(self):
        actions = []
        if self.actions:
            actions.extend(self.actions.all())
        if self.role:
            actions.extend(self.role.actions.all())
        return actions

    def get_valid_actions(self):
        actions = self.get_actions()
        today = datetime.today()

        if not self.from_date:
            self.from_date = today - timedelta(days=1)
        if not self.to_date:
            self.to_date = today + timedelta(days=1)

        if today > self.from_date and today < self.to_date:
            return actions
        return []

    def get_object(self):

        if not self.object_id:
            return "any"

        return self.content_type.get_object_for_this_type(id=self.object_id)