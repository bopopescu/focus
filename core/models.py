# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from django.db.models.query_utils import Q
from core.managers import PersistentManager
from django.db import models
import settings
from widgets import get_hexdigest, check_password
from . import Core
from inspect import isclass

"""
The Company class.
All users belong to a company, therefore all objects belongs to a company, like projects, orders...
A user can only see objects within the same company.
 * An exception to this, if the user is a guest in another companys project.
"""
class Company(models.Model):
    name = models.CharField(max_length=80)
    adminGroup = models.ForeignKey("Group", related_name="companiesWhereAdmin", null=True, blank=True)

    def __unicode__(self):
        return self.name

class User(models.Model):
    """
    Users within the Django authentication system are represented by this model.

    Username and password are required. Other fields are optional.
    """
    username = models.CharField(('username'), max_length=30, unique=True, help_text=(
    "Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    email = models.EmailField(('e-mail address'), blank=True)
    password = models.CharField(('password'), max_length=128, help_text=(
    "Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(('active'), default=True, help_text=(
    "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
    is_superuser = models.BooleanField(('superuser status'), default=False, help_text=(
    "Designates that this user has all permissions without explicitly assigning them."))
    last_login = models.DateTimeField(('last login'), default=datetime.now)
    date_joined = models.DateTimeField(('date joined'), default=datetime.now)

    company = models.ForeignKey(Company, blank=True, null=True, related_name="%(app_label)s_%(class)s_users")
    canLogin = models.BooleanField(default=True)
    profileImage = models.FileField(upload_to="uploads/profileImages", null=True, blank=True)
    deleted = models.BooleanField()

    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.username

    def get_company(self):

        if self.company:
            return self.company
        return None

    def set_company(self):
        self.company = Core.current_user().get_company()
        self.save()

    def get_company_admingroup(self):

        if not self.company:
            return None
        if not self.company.adminGroup:
            return None
        
        return self.company.adminGroup

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def set_password(self, raw_password):
        import random

        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
        self.save()

    def logged_in(self):
        return True

    def get_new_notifications(self):
        notifications = self.notifications
        return notifications.filter(read=False)


    def getProfileImage(self):
        if self.profileImage:
            return "/media/%s" % self.profileImage

        return "/media/images/avatar.jpg"

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        # Backwards-compatibility check. Older passwords won't include the
        # algorithm or salt.
        if '$' not in self.password:
            is_correct = (self.password == get_hexdigest('md5', '', raw_password))
            if is_correct:
            # Convert the password to the new, more secure format.
                self.set_password(raw_password)
                self.save()
            return is_correct
        return check_password(raw_password, self.password)

    def grant_role(self, role, object):
        #Get info about the object

        """
        Make it possible to set permissions for classes
        """
        object_id = 0
        if not isclass(object):
            object_id = object.id

        content_type = ContentType.objects.get_for_model(object)

        act = Role.objects.get(name=role)

        perm = Permission(
                role=act,
                user=self,
                content_type=content_type,
                object_id=object_id
                )
        perm.save()


    def grant_permissions (self, actions, object, **kwargs):
        from_date = None
        to_date = None
        negative = False

        """
        Set time limits, if set in func-call
        """
        if 'from_date' in kwargs:
            from_date = kwargs['from_date']
        if 'to_date' in kwargs:
            to_date = kwargs['to_date']

        """
        Set negative to negative value in kwargs
        """
        if 'negative' in kwargs:
            negative = True

        """
        Make it possible to set permissions for classes
        """
        object_id = 0
        if not isclass(object):
            object_id = object.id

        """
        For making it possible to give both list and string for permission adding.
        """
        if(isinstance(actions, str)):
            act = Action.objects.filter(name=actions)
        else:
            act = Action.objects.filter(name__in=actions)

        #Get info about the object
        content_type = ContentType.objects.get_for_model(object)

        perm = Permission(
                user=self,
                content_type=content_type,
                object_id=object_id,
                from_date=from_date,
                to_date=to_date,
                negative=negative,
                )
        perm.save()

        for p in act:
            perm.actions.add(p)

        perm.save()

        return perm

    def has_permission_to (self, action, object, id=None, any=False):
        if isinstance(object, str):
            raise Exception(
                    'Argument 2 in user.has_permission_to was a string; The proper syntax is has_permission_to(action, object)!')

        #if isinstance(action, str):
        #   action = [action]

        #If in debug and superadmin user is logged in, always return true
        if settings.DEBUG and Core.current_user().id == 1:
            return True

        content_type = ContentType.objects.get_for_model(object)

        object_id = 0
        if not isclass(object):
            object_id = object.id

        action = Action.objects.get(name=action.upper())
        allAction = Action.objects.get(name="ALL")

        #Check for negative permissions, if negative permission granted, deny
        negativePerms = Permission.objects.filter(content_type=content_type,
                                                  object_id=object_id,
                                                  user=self,
                                                  negative=True,
                                                  )

        for perm in negativePerms:
            if action in perm.get_valid_actions():
                return False
            if allAction in perm.get_valid_actions():
                return False
            
        #Checks if the user is permitted manually
        perms = Permission.objects.filter(content_type=content_type,
                                          object_id=object_id,
                                          user=self,
                                          negative=False,
                                          )

        for perm in perms:
            if action in perm.get_valid_actions():
                return True

            if allAction in perm.get_valid_actions():
                return True

        for group in self.groups.all():
            if group.has_permission_to(action, object, id=id, any=any):
                return True

        return False

    def get_permissions(self):
        permissions = []

        permissions.extend(Permission.objects.filter(user = self))

        for group in self.groups.all():
            permissions.extend(Permission.objects.filter(user = self))

        return set(permissions)


    def getPermittedObjects(self, action, model):
        content_type = ContentType.objects.get_for_model(object)

        permittedObjects = content_type.objects.all()

        for obj in content_type.objects.all():
            if not self.has_permission_to(action, obj):
                permittedObjects.exclude(id=obj.id)

        return permittedObjects

class AnonymousUser(User):
    id = 0
    user_ptr_id = 0

    class Meta:
        proxy = True

    # This is probably an ugly hack...
    # but it got it working with django 1.2, anyway, its just for testing
    class State:
        db = "default"

    _state = State

    def __init__ (self):
        self.id = 0
        self.username = 'anonymous'
        self.name = 'Not'
        self.surname = 'logged in'
        self.company = None

    def __unicode__(self):
        return "AnonymousUser"

    def logged_in (self):
        """ Anonymous users are never logged in, duh! :) """
        return False


    def is_authenticated(self):
        return False

"""
Memberships, user can be members of memberships, which can have permissions for instance
"""
class Group(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Group', related_name="children", null=True)
    members = models.ManyToManyField(User, related_name="groups")
    company = models.ForeignKey(Company, related_name="groups", null=True)
    deleted = models.BooleanField()

    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.name

    def addMember(self, user):
        self.members.add(user)
        self.save()

    def grant_role(self, role, object):
        #Get info about the object

        """
        Make it possible to set permissions for classes
        """
        object_id = 0
        if not isclass(object):
            object_id = object.id

        content_type = ContentType.objects.get_for_model(object)

        act = Role.objects.get(name=role)

        perm = Permission(
              role=act,
              group=self,
              content_type=content_type,
              object_id=object_id
              )

        perm.save()


    def save(self, *args, **kwargs):
        new = False
        if not id:
            new = True

        super(Group, self).save()

        #Give the user who created this ALL permissions on object, if new
        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)


    def grant_permissions (self, actions, object, **kwargs):
        from_date = None
        to_date = None
        negative = False

        """
        Set time limits, if set in func-call
        """
        if 'from_date' in kwargs:
            from_date = kwargs['from_date']
        if 'to_date' in kwargs:
            to_date = kwargs['to_date']

        """
        Set negative to negative value in kwargs
        """
        if 'negative' in kwargs:
            negative = True

        """
        Make it possible to set permissions for classes
        """
        object_id = 0
        if not isclass(object):
            object_id = object.id

        """
        For making it possible to give both list and string for permission adding.
        """
        if(isinstance(actions, str)):
            act = Action.objects.filter(name=actions)
        else:
            act = Action.objects.filter(name__in=actions)


        #Get info about the object
        content_type = ContentType.objects.get_for_model(object)

        perm = Permission(
                group=self,
                content_type=content_type,
                object_id=object_id,
                from_date=from_date,
                to_date=to_date,
                negative=negative,
                )
        perm.save()

        for p in act:
            perm.actions.add(p)

        perm.save()

    def has_permission_to (self, action, object, id=None, any=False):
        if isinstance(object, str):
            raise Exception(
                    'Argument 2 in user.has_permission_to was a string; The proper syntax is has_permission_to(action, object)!')

        content_type = ContentType.objects.get_for_model(object)

        object_id = 0
        if not isclass(object):
            object_id = object.id

        action = Action.objects.get(name=action)
        allAction = Action.objects.get(name="ALL")


        #Checks if the group is permitted
        perms = Permission.objects.filter(content_type=content_type,
                                          object_id=object_id,
                                          group=self,
                                          negative=False,
                                          )
        
        for perm in perms:

            if action in perm.get_valid_actions():
                return True

            if allAction in perm.get_valid_actions():
                return True
            
        if self.parent:
            return self.parent.has_permission_to(action, object, id=id, any=any)

        return False


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

        super(Log, self).save()


"""
Actions("ADD","EDIT","VIEW"..)
"""
class Action(models.Model):
    name = models.CharField(max_length=40)
    verb = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

"""
ROLES ("Leader", "Member"..)
You can grant a user role on objects by doing:

    user.grant_role("Member", object)

You can add actions to a Role by doing

    Role.grant_actions("DELETE")
or
    Role.grant_actions(['DELETE','EDIT'])
"""
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


class Permission(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="permissions")
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, blank=True, null=True, related_name="permissions")
    group = models.ForeignKey(Group, blank=True, null=True, related_name='permissions')
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
        return self.content_type.get_object_for_this_type(id=self.object_id)


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
            self.company = Core.current_user().company

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
            for us in self.whoHasPermissionTo('VIEW'):
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


"""
Adding some initial data to the model when run syncdb
"""

def initial_data ():
    Action.objects.get_or_create(name='ALL', verb='all', description='all actions on an object')
    Action.objects.get_or_create(name='CREATE', verb='created', description='create an object')
    Action.objects.get_or_create(name='EDIT', verb='edited', description='edit an object')
    Action.objects.get_or_create(name='DELETE', verb='deleted', description='delete an object')
    Action.objects.get_or_create(name='VIEW', verb='viewed', description='view an object')
    Action.objects.get_or_create(name='APPROVE', verb='approved', description='approve an object')
    Action.objects.get_or_create(name='LIST', verb='listed', description='list instances of an object')
    Action.objects.get_or_create(name='REGISTER', verb='registered for',
                                 description='register for something (event, committee, etc)')
    Action.objects.get_or_create(name='UNREGISTER', verb='unregistered from',
                                 description='unregister from something (event, etc)')
    Action.objects.get_or_create(name='FAVORITE', verb='favorited', description='favorite/star something (event etc)')
    Action.objects.get_or_create(name='MANAGE', verb='managed', description='manage something (companies etc)')

    #Generates som standard roles
    Role.objects.create(name="Admin", description="Typisk leder, kan gjøre alt")
    Role.objects.create(name="Responsible", description="Ansvarlig, kan se,endre")
    Role.objects.create(name="Member", description="Typisk medlem, kan se")
    Role.objects.create(name="Owner", description="Typisk den som opprettet objektet")

    leader = Role.objects.get(name="Admin")
    leader.grant_actions(["ALL"])

    owner = Role.objects.get(name="Owner")
    owner.grant_actions(["EDIT", "VIEW", "DELETE"])

    member = Role.objects.get(name="Member")
    member.grant_actions(["VIEW", "LIST"])

    #Other default objects
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

    u, created = User.objects.all().get_or_create(username="test",
                                                  first_name="Test1",
                                                  canLogin=True,
                                                  last_name="user",
                                                  company=comp,
                                                  is_active=True)
    u.set_password("test")
    u.save()

    u, created = User.objects.all().get_or_create(username="test2",
                                                  first_name="Test2",
                                                  canLogin=True,
                                                  company=comp,
                                                  last_name="user",
                                                  is_active=True)

    u.set_password("test2")
    u.save()

    u, created = User.objects.all().get_or_create(username="test3",
                                                  first_name="Test3",
                                                  canLogin=True,
                                                  company=comp,
                                                  last_name="user",
                                                  is_active=True)

    u.set_password("test3")
    u.save()