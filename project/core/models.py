# -*- coding: utf-8 -*-
from django.core.cache import cache
from core import Core
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from core.auth.company.models import Company
from core.auth.log.models import Log, Notification
from core.auth.permission.models import Role, Action, Permission
from core.auth.user.models import User
from core.managers import PersistentManager
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

def createTuple(object):
    oldObject = object.get_object()

    data = {}

    for i in object._meta.fields:
        if i.attname.startswith('_'):
            continue

        if unicode(getattr(object, i.attname)) in ('True', 'False', 'None') or isinstance(getattr(object, i.attname),
                                                                                          (int, long, float)):
            data[i.attname] = [getattr(object, i.attname), unicode(i.verbose_name)]
        else:
            data[i.attname] = [unicode(getattr(object, i.attname)), unicode(i.verbose_name)]

    return data


class PersistentModel(models.Model):
    trashed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=datetime.now())
    date_edited = models.DateTimeField(default=datetime.now())
    creator = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_created")
    editor = models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_edited")
    company = models.ForeignKey(Company, blank=True, null=True, default=None, related_name="%(class)s_companies")

    objects = PersistentManager()
    #objects = models.Manager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, **kwargs):
        action = "EDIT"
        if not self.id:
            action = "ADD"
            self.date_created = datetime.now()
            self.creator = Core.current_user()
            self.company = Core.current_user().company

        self.editor = Core.current_user()
        self.date_edited = datetime.now()

        changes = createTuple(self)
        super(PersistentModel, self).save()

        #Clear cache
        cache_key = "%s_%s" % (Core.current_user().id, self.__class__.__name__)
        cache.delete(cache_key)

        #GRANT PERMISSIONS
        if action == "ADD":
            Core.current_user().grant_role("Admin", self)
            admin_group = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if admin_group:
                admin_group.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

        if 'noLog' not in kwargs:
            log = Log(message=changes,
                      object_id=self.id,
                      content_type=ContentType.objects.get_for_model(self.__class__),
                      action=action,
                      )
            log.save()

            if 'noNotification' not in kwargs:
                for us in self.who_has_permission_to('VIEW'):
                    if us == Core.current_user():
                        continue
                    Notification(recipient=us,
                                 log=log,
                                 ).save()

    def trash(self, **kwargs):
        self.trashed = True
        super(PersistentModel, self).save()

    def restore(self, *args, **kwargs):
        self.trashed = False
        super(PersistentModel, self).save()

    def delete(self, **kwargs):
        self.deleted = True
        super(PersistentModel, self).save()

    def history(self):
        return Log.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__),
                                  object_id=self.id)

    def get_object (self):
        """
        Gets the object even if it's deleted.
        """

        model = ContentType.objects.get_for_model(self.__class__).model_class()

        try:
            return model.all_objects.get(id=self.id)

        except model.DoesNotExist:
            return "[Object does not exist]"


    """
    who_has_permission_to
    returns a list of users who are permitted perform actions on the object
    """

    def who_has_permission_to(self, perm):
        try:
            content_type = ContentType.objects.get_for_model(self)
            id = self.id
            users = []

            object = content_type.get_object_for_this_type(id=id)

            perm = Action.objects.get(name=perm.upper())
            adminPerm = Action.objects.get(name="ALL")

            for u in Permission.objects.filter(content_type=content_type, negative=False, object_id=id):
                if perm in u.get_valid_actions():
                    if u.user and u.user not in users:
                        users.append(u.user)

                    if u.group:
                        for user in u.group.members.all():
                            if user and user not in users:
                                users.append(user)

                if adminPerm in u.get_valid_actions():
                    if u.user and u.user not in users:
                        users.append(u.user)

                    if u.group:
                        for user in u.group.members.all():
                            if user and user not in users:
                                users.append(user)

            return users
        except:
            return []

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Comment(PersistentModel):
    text = models.TextField()

    # What object is this a comment for?
    object = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    attachment = models.FileField(upload_to="comments", storage=fs, null=True)

    class Meta:
        ordering = ['date_created']

    def __unicode__ (self):
        return self.text

"""
Adding some initial data to the model when run syncdb
"""

def initial_data ():
    print "creating Actions"
    Action.objects.get_or_create(name='ALL', verb='all', description='all actions on an object')
    Action.objects.get_or_create(name='CREATE', verb='created', description='create an object')
    Action.objects.get_or_create(name='EDIT', verb='edited', description='edit an object')
    Action.objects.get_or_create(name='CONFIGURE', verb='edited', description='edit an object')
    Action.objects.get_or_create(name='MANAGE', verb='mange', description='manage an object')
    Action.objects.get_or_create(name='DELETE', verb='deleted', description='delete an object')
    Action.objects.get_or_create(name='VIEW', verb='viewed', description='view an object')
    Action.objects.get_or_create(name='LIST', verb='listed', description='list instances of an object')
    Action.objects.get_or_create(name='LISTALL', verb='listed all', description='list of all objects')
    Action.objects.get_or_create(name='LISTDELETED', verb='listed deleted', description='list deleted')
    Action.objects.get_or_create(name='LISTARCHIVE', verb='listed deleted', description='list deleted')
    Action.objects.get_or_create(name='LISTREADYINVOICE', verb='listed deleted', description='list deleted')
    print "Done"

    print "creating Roles"
    #Generates som standard roles
    Role.objects.get_or_create(name="Admin", description="Typisk leder, kan gjøre alt")
    Role.objects.get_or_create(name="Responsible", description="Ansvarlig, kan se,endre")
    Role.objects.get_or_create(name="Member", description="Typisk medlem, kan se")
    Role.objects.get_or_create(name="Owner", description="Typisk den som opprettet objektet")
    print "Done"

    leader = Role.objects.get(name="Admin")
    leader.grant_actions(["ALL"])

    owner = Role.objects.get(name="Owner")
    owner.grant_actions(["EDIT", "VIEW", "DELETE"])

    member = Role.objects.get(name="Member")
    member.grant_actions(["VIEW", "LIST"])

    #Other default objects
    comp = Company.objects.get_or_create(name="Superfirma AS", days_into_next_month_hourregistration=4)[0]
    comp.save()

    a, created = User.all_objects.get_or_create(username="superadmin",
                                                first_name="SuperAdmin",
                                                last_name="", )

    a.company = comp
    a.is_superuser = True
    a.canLogin = True
    a.is_staff = True
    a.set_password("superpassord")
    a.save()

    u, created = User.all_objects.get_or_create(username="test",
                                                first_name="Test1",
                                                )
    u.company = comp
    u.set_password("test")
    u.save()