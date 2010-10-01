from django.db import models
from django.contrib.auth.models import User, UserManager, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from managers import PersistentManager
from django.conf import settings
from core.middleware import *
import datetime

"""
For auto-version of objects
"""
from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""
    
    
"""
The Company class.
All users belong to a company, therefore all objects belongs to a company, like projects, orders...
A user can only see objects within the same company.
 * An exception to this, if the user is a guest in another companys project.
"""
class Company (models.Model):
    name = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name

"""
The "all mighty" model, all other models inherit from this one. 
Contains all the useful fields like who created and edited the object, and when it was done.
It also automatic saves the information about the user interaction with the object.
"""
class PersistentModel(models.Model):
    deleted = models.BooleanField(default = False)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_edited = models.DateTimeField(default=datetime.datetime.now())    

    creator =   models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_created")
    editor  =   models.ForeignKey(User, blank=True, null=True, default=None, related_name="%(class)s_edited")
    company =   models.ForeignKey(Company, blank=True, null=True, default=None, related_name="%(class)s_edited")
    
    objects = PersistentManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        
    def save(self, **kwargs):
        if not self.id:
            self.creator = get_current_user()
            self.company = get_current_user().get_profile().company
            
        self.editor = get_current_user()
            
        
        self.date_edited = datetime.datetime.now()    
        
        super(PersistentModel, self).save()

    def delete(self, **kwargs):
        self.deleted = True
        super(PersistentModel, self).save()     
   

admin.site.register(Company, ModelAdmin)

"""
Memberships, user can can be members of memberships, which can have permissions for instance
"""
class Membership(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name="memberships")
    company = models.ForeignKey(Company, blank=True, null=True, related_name="memberships")
    
    def __unicode__(self):
        return self.name
    
admin.site.register(Membership, ModelAdmin)

"""
ROLES
"""
class Role(models.Model):
    name = models.CharField(max_length=200)
    permission = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, blank=True, null=True, related_name="roles")
    membership = models.ForeignKey(Membership, blank=True, null=True, related_name='roles')
    
    content_type = models.ForeignKey(ContentType)

    def __unicode__(self):
        return unicode(self.content_type)


admin.site.register(Role, ModelAdmin)


"""
Adding object permissins to object, using a content_type for binding with all kinds of objects
"""
class ObjectPermission(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name="permissions")
    membership = models.ForeignKey(Membership, blank=True, null=True, related_name='permissions')
        
    deleted = models.BooleanField()
    
    #General permissions
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    negative = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.content_type.get_object_for_this_type(id=self.object_id))

admin.site.register(ObjectPermission, ModelAdmin)

from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

"""
Userprofiles, for adding additional informartion about the user
"""
class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True, related_name="%(app_label)s_%(class)s_users")
    
    def __unicode__(self):
        return "Profile for: %s" % self.user

admin.site.register(UserProfile)

"""
Keeping users and their userprofile in sync, when creating a user, a userprofile is createad as well.
"""

def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        try:
            up.company = get_current_user().get_profile()
        except:
            up.save()

post_save.connect(create_profile, sender=User)

 
"""
Adding some initial data to the model when run syncdb
"""

from app.timetracking.models import *
def initial_data ():     
    
    comp = Company(name="Focus AS")
    comp.save()
    
    a, created = User.objects.get_or_create(username="superadmin", first_name="SuperAdmin", last_name="", is_superuser = True, is_staff=True, is_active=True)
    a.set_password("superpassord")
    a.save()

    u,created = User.objects.get_or_create(username="bjarte", first_name="Bjarte", last_name="Hatlenes", is_active=True)
    u.set_password("superpassord")
    u.save()
    u.get_profile().company = comp
    u.get_profile().save()