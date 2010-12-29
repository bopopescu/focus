from django.template.loader import render_to_string
import django.forms as forms
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor, md5_constructor


class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)

        name_id = name
        if str(name[len(name) - 1]) is "s":
            name_id = name[0:len(name) - 1]

        if str(name[len(name) - 1]) is not "s":
            name += "s"

        popupplus = render_to_string("popupplus.html", {'field': name, 'field_id': name_id})

        return html + popupplus

class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)

        if str(name[len(name) - 1]) is not "s":
            name += "s"

        name_id = name

        popupplus = render_to_string("popupplus.html", {'field': name, 'field_id': name_id})
        return html + popupplus


class DatePickerField(forms.DateInput):
    def render(self, name, *args, **kwargs):
        html = super(DatePickerField, self).render(name, *args, **kwargs)
        datepicker = render_to_string("datepicker.html", {'field': name})
        return html + datepicker

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
