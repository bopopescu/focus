# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from core.managers import PersistentManager
from . import Core
from core.user import Company, User
from core.log import Log

"""
The "all mighty" model, all other models inherit from this one. 
Contains all the useful fields like who created and edited the object, and when it was done.
It also automatically saves the information about the user interaction with the object.
"""

class PersistentModel(models.Model):
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now())
    date_edited = models.DateTimeField(default=datetime.now())

    creator = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_created")
    editor = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_edited")
    company = models.ForeignKey(Company, blank=True, null=True, default=None, related_name="%(class)s_edited")

    objects = PersistentManager()
    #objects = models.Manager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, **kwargs):
        action = "EDIT"
        if not self.id:
            action = "ADD"
            self.creator = Core.current_user()
        #self.company = get_current_company()

        #self.editor = get_current_user()
        self.date_edited = datetime.now()
        super(PersistentModel, self).save()

        if 'noLog' not in kwargs:
            msg = "endret"
            if action == "ADD":
                msg = "opprettet"

            Log(message="%s %s %s" % (Core.current_user(), msg, self),
                object_id=self.id,
                content_type=ContentType.objects.get_for_model(self.__class__),
                action=action,
                ).save()

        if 'noNotification' not in kwargs:
            for us in self.whoHasPermissionTo('view'):
                if us == Core.current_user():
                    continue
                Notification(text="Dette er en test",
                             recipient=us,
                             object_id=self.id,
                             content_type=ContentType.objects.get_for_model(self.__class__)
                             ).save()

    def delete(self, **kwargs):
        self.deleted = True
        super(PersistentModel, self).save()

    def recover(self, *args, **kwargs):
        self.deleted = False
        super(PersistentModel, self).save()

    """
    whoHasPermissionTo
    returns a list of users who are permitted perform actions on the object
    """

    def whoHasPermissionTo(self, perm):
        try:
            content_type = ContentType.objects.get_for_model(self)
            id = self.id
            users = []

            for u in Permission.objects.filter(content_type=content_type, negative=False, object_id=id,
                                               **{'can_%s' % perm: True}):
                if u.user and u.user not in users:
                    users.append(u.user)
                if u.membership:
                    for user in u.membership.users.all():
                        if user and user not in users:
                            users.append(user)
            return users
        except:
            return []


"""
Adding some initial data to the model when run syncdb
"""

def initial_data ():
    comp = Company(name="Focus AS")
    comp.save()

    a, created = User.objects.all().get_or_create(username="superadmin",
                                                  first_name="SuperAdmin",
                                                  last_name="",
                                                  canLogin=True,
                                                  is_superuser=True,
                                                  is_staff=True,
                                                  is_active=True)
    a.set_password("superpassord")
    a.save()

    u, created = User.objects.all().get_or_create(username="testgdfg",
                                                  first_name="Test",
                                                  last_name="User",
                                                  is_active=True)
    u.set_password("test")
    u.save()

    #u.get_profile().company = comp
    #u.get_profile().save()

    u, created = User.objects.all().get_or_create(username="test2fdgdf",
                                                  first_name="Test2",
                                                  last_name="User2",
                                                  is_active=True)
    u.set_password("test2")
    u.save()

#u.get_profile().company = comp
#u.get_profile().save()