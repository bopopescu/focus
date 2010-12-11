from django.forms.models import modelformset_factory
from django.forms import ModelForm
from models import *
from core.middleware import *
from core.models import *

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