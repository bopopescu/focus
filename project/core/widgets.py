from datetime import datetime
from django.forms.widgets import Input
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor, md5_constructor
import django.forms as forms


class SelectWithPop(forms.Select):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(SelectWithPop, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)

        name_id = name
        if str(name[len(name) - 1]) is "s":
            name_id = name[0:len(name) - 1]

        if str(name[len(name) - 1]) is not "s":
            name += "s"

        popupplus = render_to_string("popupplus.html", {'field': name,
                                                        'field_id': name_id,
                                                        'add_ajax_url': self.app.add_ajax_url(),
                                                        'form': self.app.simpleform()})

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
    def __init__(self, *args, **kwargs):
        self.from_date = None
        self.to_date = None

        if 'from_date' in kwargs:
            self.from_date = datetime.strptime(kwargs['from_date'], "%d.%m.%Y")
            del kwargs['from_date']

        if 'to_date' in kwargs:
            self.to_date = datetime.strptime(kwargs['to_date'], "%d.%m.%Y")
            del kwargs['to_date']

        super(DatePickerField, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(DatePickerField, self).render(name, *args, **kwargs)
        datepicker = render_to_string("datepicker.html",
                                      {'field': name, 'from_date': self.from_date, 'to_date': self.to_date})
        return html + datepicker

class MaskedField(Input):
    def __init__(self, *args, **kwargs):
        self.format = None

        if 'format' in kwargs:
            self.format = kwargs['format']
            del kwargs['format']

        super(MaskedField, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(MaskedField, self).render(name, *args, **kwargs)
        masked = render_to_string("masked.html", {'field': name, 'maskedFormat': self.format})
        return html + masked

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
