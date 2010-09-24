from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from core.models import ObjectPermission

class ObjectPermBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_authenticated():
            return False

        if obj is None:
            return False
        
        try:
            ct = ContentType.objects.get_for_model(obj)
        except Exception:
            return False
        
        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False


        p = ObjectPermission.objects.filter(content_type=ct,
                                            object_id=obj.id,
                                            user=user_obj)
        
        if p.filter(negative=True).exists():
            return False

        if(self.check_users_membership_for_permissions(user_obj, perm, obj)):
            return True
             
        return p.filter(**{'can_%s' % perm: True}).exists()
            
    def check_users_membership_for_permissions(self, user, perm, obj = None):
        for membership in user.memberships.all():
            if self.membership_has_perm(membership, perm, obj):
                return True
        return False

    def membership_has_perm(self, membership_obj, perm, obj=None):
        if obj is None:
            return False    
        try:
            ct = ContentType.objects.get_for_model(obj)
        except Exception:
            return False
        
        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        p = ObjectPermission.objects.filter(content_type=ct,
                                            object_id=obj.id,
                                            membership=membership_obj)
                
        return p.filter(**{'can_%s' % perm: True}).exists()        