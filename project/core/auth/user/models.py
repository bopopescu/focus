# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from inspect import isclass
from core import Core
from core.managers import PersistentManager
from core.widgets import get_hexdigest, check_password
from core.auth.company.models import Company
from core.auth.permission.models import Permission, Action, Role
from django.utils.translation import ugettext as _
from django.core import urlresolvers
import time
import os
from django.utils import translation

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

    language = models.CharField(max_length=30, choices=settings.LANGUAGES, default="nb")
    
    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return self.get_full_name()

    def get_company(self):
        cache_key = "%s_%s_%s" % ("USER",self.id, "COMPANY")

        if cache.get(cache_key):
            return cache.get(cache_key)
        else:
            result = None
            if self.company:
                result = self.company
            cache.set(cache_key, result)
            return result

    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.logs.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("User has a history, check history tab. "))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    def use_user_language(self, request):
        language = "en"
        for lang in settings.LANGUAGES:
            if self.language in lang[0]:
                language = lang[0]

        request.session['language'] = language
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def get_view_url(self):
        return urlresolvers.reverse('app.admin.views.user.view', args=("%s" % self.id,))

    def save(self, *args, **kwargs):

        action = "EDIT"
        
        if not self.id:
            action = "ADD"

        super(User, self).save()

        if action == "ADD":
            Core.current_user().grant_role("Owner", self)
            admin_group = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if admin_group:
                admin_group.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

    def set_valid_period(self, **kwargs):
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

    def generate_valid_period(self, *args, **kwargs):
        now = datetime.now()

        if 'today' in kwargs:
            now = datetime.strptime(kwargs['today'], "%d.%m.%Y")

        daysIntoNextMonthTimetracking = 0
        if self.company:
            daysIntoNextMonthTimetracking = self.company.get_days_into_next_month()

        #if true, user can still edit last month
        if daysIntoNextMonthTimetracking >= now.day:
            #if January, the user should be able to edit December last year
            if now.month == 1:
                from_date = datetime(now.year - 1, 12, 1)
                to_date = datetime(now.year, 1, now.day)

            #if rest of the year, set last month editable
            else:
                from_date = datetime(now.year, now.month - 1, 1)
                to_date = datetime(now.year, now.month, now.day)

        #else, the user can edit from first this month -> today
        else:
            from_date = datetime(now.year, now.month, 1)
            to_date = datetime(now.year, now.month, now.day)

        #check if user has extended the period
        if self.validEditHourRegistrationsToDate and self.validEditHourRegistrationsToDate > to_date:
            to_date = self.validEditHourRegistrationsToDate

        #check if user has extended the period
        if self.validEditHourRegistrationsFromDate and self.validEditHourRegistrationsFromDate < from_date:
            from_date = self.validEditHourRegistrationsFromDate

        return [from_date.strftime("%d.%m.%Y"), to_date.strftime("%d.%m.%Y")]

    def can_edit_hour_date(self, date, *args, **kwargs):
        now = datetime.now()
        period = self.generate_valid_period(*args, **kwargs)

        if 'today' in kwargs:
            now = datetime.strptime(kwargs['today'], "%d.%m.%Y")
            period = self.generate_valid_period(today=kwargs['today'])

        date = time.mktime(time.strptime("%s" % (date), "%d.%m.%Y"))
        from_date = time.mktime(time.strptime("%s" % (period[0]), "%d.%m.%Y"))
        to_date = time.mktime(time.strptime("%s" % (period[1]), "%d.%m.%Y"))

        if date >= from_date and date <= to_date:
            return True

        return False

    def can_edit_hourregistration(self, hourRegistration, *args, **kwargs):
        return self.can_edit_hour_date(hourRegistration.date.strftime("%d.%m.%Y"), *args, **kwargs)

    def set_company(self):
        self.company = Core.current_user().get_company()
        self.save()

    def get_company_admingroup(self):
        if not self.company:
            return None
        if not self.company.admin_group:
            return None

        return self.company.admin_group

    def get_company_allemployeesgroup(self):
        if not self.company:
            return None
        if not self.company.all_employees_group:
            return None

        return self.company.all_employees_group

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_full_name(self):
        #Returns the first_name plus the last_name, with a space in between.
        name = u'%s %s' % (self.first_name, self.last_name)

        return name.strip()

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

        #Invalidate cache for user
        cache_key = "%s_%s" % (Core.current_user().id, self.__class__.__name__)
        cache.delete(cache_key)

    def grant_permissions (self, actions, object, **kwargs):
        from_date = None
        to_date = None
        negative = False

        #Set time limits, if set in func-call
        if 'from_date' in kwargs:
            from_date = kwargs['from_date']
        if 'to_date' in kwargs:
            to_date = kwargs['to_date']

        #Set negative to negative value in kwargs
        if 'negative' in kwargs:
            negative = True

        #Make it possible to set permissions for classes
        object_id = 0
        if not isclass(object):
            object_id = object.id

        #For making it possible to give both list and string for permission adding.
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

        #Invalidate cache for user
        cache_key = "%s_%s" % (Core.current_user().id, self.__class__.__name__)
        cache.delete(cache_key)

        return perm

    def has_permission_to (self, action, object, id=None, any=False):
        if isinstance(object, str):
            raise Exception(
                'Argument 2 in user.has_permission_to was a string; The proper syntax is has_permission_to(action, object)!')

        try:
            cache_key = "%s_%s_%s" % (Core.current_user().id, action, object.__name__)
        except Exception, e:
            cache_key = "%s_%s_%s" % (Core.current_user().id, action, object.__class__.__name__)

        if cache.get(cache_key):
            return cache.get(cache_key)

        content_type = ContentType.objects.get_for_model(object)

        if settings.DEBUG and Core.current_user().is_superuser:
            cache.set(cache_key, True, 5000)
            return True

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
                cache.set(cache_key, False, 5000)
                return False
            if allAction in perm.get_valid_actions():
                cache.set(cache_key, False, 5000)

                return False

        #Checks if the user is permitted manually
        perms = Permission.objects.filter(content_type=content_type,
                                          object_id=object_id,
                                          user=self,
                                          negative=False,
                                          )

        for perm in perms:
            if action in perm.get_valid_actions():
                cache.set(cache_key, True, 5000)

                return True

            if allAction in perm.get_valid_actions():
                cache.set(cache_key, True, 5000)

                return True

        for group in self.groups.all():
            if group.has_permission_to(action, object, id=id, any=any):
                cache.set(cache_key, True, 5000)

                return True

        cache.set(cache_key, False, 5000)
        return False

    def get_permissions(self, content_type=None):
        permissions = []

        groups = self.groups.all()

        if content_type:
            return Permission.objects.filter(content_type=content_type).filter(Q(user=self) | Q(group__in=groups))

        return Permission.objects.filter(Q(user=self) | Q(group__in=groups))


    def get_permitted_objects(self, action, model):
        content_type = ContentType.objects.get_for_model(model)
        action_string = action

        cache_key = "%s_%s_%s" % (self.id, model.__name__, action_string)

        if cache.get(cache_key) and action_string in cache.get(cache_key):
            permitted = cache.get(cache_key)["%s"%action_string]
        else:

            action = Action.objects.get(name=action)
            allAction = Action.objects.get(name="ALL")

            tree = {}
            permitted = []

            permissions = self.get_permissions(content_type)
            for perm in permissions:
                if not perm.object_id in tree:
                    tree[perm.object_id] = []


                if perm.actions:
                    tree[perm.object_id].extend(perm.actions.all())

                    if action in tree[perm.object_id] or allAction in tree[perm.object_id]:
                        continue

                if perm.role:
                    tree[perm.object_id].extend(perm.role.actions.all())

            for node in tree:
                if allAction in tree[node]:
                    permitted.append(node)
                elif action in tree[node]:
                    permitted.append(node)

            permitted = list(model.objects.filter(id__in=permitted).select_related())
            
            cache.set(cache_key, {'%s'%action_string: permitted}, 1200)

        return permitted

class AnonymousUser(User):
    id = 0
    user_ptr_id = 0

    class Meta:
        proxy = True

    class State:
        db = "default"

    _state = State

    def __init__ (self):
        self.id = 0
        self.username = 'anonymous'
        self.name = 'Not'
        self.surname = 'logged in'
        self.company = None

    def get_company(self):
        return None

    def __unicode__(self):
        return "AnonymousUser"

    def logged_in (self):
        """ Anonymous users are never logged in, duh! :) """
        return False


    def is_authenticated(self):
        return False