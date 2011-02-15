"""
from django.forms.models import modelformset_factory
from django.forms import ModelForm
from models import *
from core.middleware import *
from core.models import *


Not in use for now

class PermissionForm(ModelForm):    
    class Meta:
        model = Permission
        exclude = ('content_type', 'object_id')
        
    def __init__(self,*args,**kwargs):
        super (PermissionForm,self ).__init__(*args,**kwargs) # populates the post
        company = get_current_user().get_profile().company
        self.fields['user'].queryset = User.objects.filter(userprofile__company=company)
        self.fields['membership'].queryset = Membership.objects.filter(company=company)
        
        self.fields['user'].widget.attrs['class'] = "small"
        self.fields['membership'].widget.attrs['class'] = "small"
        
PermFormSet = modelformset_factory(Permission, extra=3, form=PermissionForm)

"""
from django.contrib.contenttypes.models import ContentType
from core.models import Comment
from django.forms.models import ModelForm


class CommentForm (ModelForm):

    def __init__ (self, object, *args, **kwargs):

        object_id = object.id
        content_type = ContentType.objects.get_for_model(object)
        # If there is no instance, make a fake one!
        if not 'instance' in kwargs:
            kwargs['instance'] = Comment(object_id = object_id, content_type = content_type)

        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)