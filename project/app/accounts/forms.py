from django import forms
from django.utils.translation import ugettext as _

class LoginForm (forms.Form):
    username = forms.CharField(label = _('Username'))
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput(render_value = False))
    remember = forms.BooleanField(label = _('Remember'), required = False)