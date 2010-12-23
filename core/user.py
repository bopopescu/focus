# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor

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
Memberships, user can be members of memberships, which can have permissions for instance
"""
class Membership(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Membership', related_name="children", null=True)
    members = models.ManyToManyField(User, related_name="memberships")

    def __unicode__(self):
        return self.name