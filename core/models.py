# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from core.managers import PersistentManager
from . import Core

"""
The Company class.
All users belong to a company, therefore all objects belongs to a company, like projects, orders...
A user can only see objects within the same company.
 * An exception to this, if the user is a guest in another companys project.
"""
class Company(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    algo, salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(algo, salt, raw_password)


class AnonymousUser(models.Model):
    def is_authenticated(self):
        return False

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

    def __unicode__(self):
        return self.username

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

	def has_perms(self, perm_list, obj=None):
	    return True

	def has_module_perms(self, app_label):
		return True

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

    def set_unusable_password(self):
    # Sets a value that will never be a valid hash
        self.password = UNUSABLE_PASSWORD

    def has_usable_password(self):
        return self.password != UNUSABLE_PASSWORD


"""
Userprofiles, for adding additional informartion about the user

class UserProfile(User):
    company = models.ForeignKey(Company, blank=True, null=True, related_name="%(app_label)s_%(class)s_users")
    canLogin = models.BooleanField(default=True)
    profileImage = models.FileField(upload_to="uploads/profileImages", null=True, blank=True)

    def notifications(self):
        return self.user.notifications.filter(read=False)

    def getProfileImage(self):
        if self.profileImage:
            return "/media/%s" % self.profileImage

        return "/media/images/avatar.jpg"

    def __unicode__(self):
        return "Profile for: %s" % self.user
"""

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


"""
Class for logs, saves user in action and reference to object logged
"""
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
Memberships, user can be members of memberships, which can have permissions for instance
"""
class Membership(PersistentModel):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Membership', related_name="children", null=True)
    members = models.ManyToManyField(User, related_name="memberships")

    def __unicode__(self):
        return self.name

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