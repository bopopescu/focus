# -*- coding: utf-8 -*-
from core import Core
from inspect import isclass
import os
import time
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from core.managers import PersistentManager
from core.widgets import get_hexdigest, check_password
from core.auth.company.models import Company
from core.auth.permission.models import Permission, Action, Role

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class User(models.Model):
    username = models.CharField(('username'), max_length=30, unique=True, help_text=(
    "Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    first_name = models.CharField(('first name'), max_length=60, blank=True)
    last_name = models.CharField(('last name'), max_length=60, blank=True)
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

    phone = models.CharField(max_length=30, null=True)
    birthdate = models.DateField("Bday", null=True)
    company = models.ForeignKey(Company, blank=True, null=True, related_name="%(app_label)s_%(class)s_users")
    canLogin = models.BooleanField(default=True)
    profileImage = models.ImageField(upload_to="profileImages", storage=fs, null=True, blank=True)
    deleted = models.BooleanField()

    #HourRegistrations valid period
    validEditHourRegistrationsFromDate = models.DateTimeField(null=True, verbose_name="From")
    validEditHourRegistrationsToDate = models.DateTimeField(null=True, verbose_name="To")

    hourly_rate = models.IntegerField(null=True)
    percent_cover = models.IntegerField(null=True)

    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.username

    def get_company(self):
        if self.company:
            return self.company
        return None

    def canBeDeleted(self):
        canBeDeleted = True
        reasons = []

        if self.logs.all().count() > 0:
            canBeDeleted = False
            reasons.append(_("User has a history, check history tab. "))

        if canBeDeleted:
            return (True, "OK")

        return (False, reasons)


    def save(self, *args, **kwargs):
        action = "EDIT"
        if not self.id:
            action = "ADD"

        super(User, self).save()

        if action == "ADD":
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

    def setValidPeriodManually(self, **kwargs):
        if 'toDate' in kwargs:
            if kwargs['toDate'] == "":
                self.validEditHourRegistrationsToDate = None
            else:
                self.validEditHourRegistrationsToDate = datetime.strptime(kwargs['toDate'], "%d.%m.%Y")

        if 'fromDate' in kwargs:
            if kwargs['fromDate'] == "":
                self.validEditHourRegistrationsFromDate = None
            else:
                self.validEditHourRegistrationsFromDate = datetime.strptime(kwargs['fromDate'], "%d.%m.%Y")

        self.save()

    def generateValidPeriode(self, *args, **kwargs):
        now = datetime.now()

        if 'today' in kwargs:
            now = datetime.strptime(kwargs['today'], "%d.%m.%Y")

        daysIntoNextMonthTimetracking = 0
        if self.company:
            daysIntoNextMonthTimetracking = self.company.getDaysIntoNextMonthHourRegistration()

        #If true, user can still edit last month
        if daysIntoNextMonthTimetracking >= now.day:
            #If January, the user should be able to edit December last year
            if now.month == 1:
                from_date = datetime(now.year - 1, 12, 1)
                to_date = datetime(now.year, 1, now.day)

            #If rest of the year, set last month editable
            else:
                from_date = datetime(now.year, now.month - 1, 1)
                to_date = datetime(now.year, now.month, now.day)

        #Else, the user can edit from first this month -> today
        else:
            from_date = datetime(now.year, now.month, 1)
            to_date = datetime(now.year, now.month, now.day)


        #Check if user has extended the period
        if self.validEditHourRegistrationsToDate and self.validEditHourRegistrationsToDate > to_date:
            to_date = self.validEditHourRegistrationsToDate

        if self.validEditHourRegistrationsFromDate and self.validEditHourRegistrationsFromDate < from_date:
            from_date = self.validEditHourRegistrationsFromDate

        return [from_date.strftime("%d.%m.%Y"), to_date.strftime("%d.%m.%Y")]

    def canEditHourRegistration(self, hourRegistration, *args, **kwargs):
        now = datetime.now()

        period = self.generateValidPeriode(*args, **kwargs)

        if 'today' in kwargs:
            now = datetime.strptime(kwargs['today'], "%d.%m.%Y")
            period = self.generateValidPeriode(today=kwargs['today'])

        date = time.mktime(time.strptime("%s" % (hourRegistration.date.strftime("%d.%m.%Y")), "%d.%m.%Y"))
        from_date = time.mktime(time.strptime("%s" % (period[0]), "%d.%m.%Y"))
        to_date = time.mktime(time.strptime("%s" % (period[1]), "%d.%m.%Y"))

        if date >= from_date and date <= to_date:
            return True
        return False

    def set_company(self):
        self.company = Core.current_user().get_company()
        self.save()

    def get_company_admingroup(self):
        if not self.company:
            return None
        if not self.company.adminGroup:
            return None

        return self.company.adminGroup

    def get_company_allemployeesgroup(self):
        if not self.company:
            return None
        if not self.company.allEmployeesGroup:
            return None

        return self.company.allEmployeesGroup

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
            if os.path.join("/file/", self.profileImage.name):
                return os.path.join("/file/", self.profileImage.name)

        return settings.STATIC_URL + "images/avatar.jpg"

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
        if settings.DEBUG and Core.current_user().is_superuser:
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

        for p in Permission.objects.filter(user=self):
            if not p.id in permissions:
                permissions.append(p.id)

        for group in self.groups.all():
            for p in group.get_permissions():
                if not p.id in permissions:
                    permissions.append(p.id)

        return Permission.objects.filter(id__in=permissions)

    """
    SKRIVE OM , ta utgangspunkt i permission-tabellen
    """

    def getPermittedObjects(self, action, model):
        objects = model.objects.filter()
        contenttype = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=contenttype, user=self)

        action = Action.objects.get(name=action)
        allAction = Action.objects.get(name="ALL")

        tree = {}
        permitted = []

        for perm in permissions:
            if not perm.object_id in tree:
                tree[perm.object_id] = []

            tree[perm.object_id].extend(perm.actions.all())
            tree[perm.object_id].extend(perm.role.actions.all())

        for node in tree:
            if allAction in tree[node]:
                permitted.append(node)
            if action in tree[node]:
                permitted.append(node)

        return model.objects.filter(id__in=permitted)

        """
        SLOW
        unwanted = []
        objects = model.objects.filter(company=self.get_company())

        for obj in objects:
            if not self.has_permission_to(action, obj):
                unwanted.append(obj.id)

        return objects.exclude(id__in=unwanted)
        """


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
