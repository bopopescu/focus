from datetime import datetime
from django.forms.widgets import Input
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor, md5_constructor
import django.forms as forms
from django.utils.simplejson import JSONEncoder
from django.utils.safestring import mark_safe, SafeString, SafeUnicode
from django.utils.html import escape
from django.utils.encoding import force_unicode, smart_unicode
from django.forms.widgets import flatatt
from django.conf import settings


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
                                                        'STATIC_URL': settings.STATIC_URL,
                                                        'field_id': name_id,
                                                        'add_ajax_url': self.app.add_ajax_url(),
                                                        'form': self.app.simpleform()},
                                     )

        return html + popupplus


class MultipleSelectWithPop(forms.SelectMultiple):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(MultipleSelectWithPop, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)

        if str(name[len(name) - 1]) is not "s":
            name += "s"

        name_id = name

        popupplus = render_to_string("popupplus.html", {'field': name,
                                                        'STATIC_URL': settings.STATIC_URL,
                                                        'field_id': name_id,
                                                        'add_ajax_url': self.app.add_ajax_url(),
                                                        'form': self.app.simpleform()})

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


class JQueryAutoComplete(forms.TextInput):
    def __init__(self, source=None, sourceJS=False, options={}, attrs={}):
        forms.TextInput.__init__(self)
        """source can be a list containing the autocomplete values or a
        string containing the url used for the XH-Request.

        For available options see the autocomplete sample page::
        http://jquery.bassistance.de/autocomplete/"""

        self.options = None
        self.attrs = {'autocomplete': 'off'}
        self.source = source
        self.sourceJS = sourceJS
        #self.source = source
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)

        self.attrs.update(attrs)

    def render_js(self, field_id):
        if callable(self.source):
            self.source = self.source()
        if isinstance(self.source, list):
            source = JSONEncoder().encode(self.source)
        elif (isinstance(self.source, str) or isinstance(self.source, unicode) or
              isinstance(self.source, SafeString) or isinstance(self.source, SafeUnicode)):
            if not self.sourceJS:
                source = JSONEncoder().encode({'source': escape(self.source)})
            else:
                source = self.source
        else:
            raise ValueError('source type is not valid')

        options = ''
        if self.options:
            options += ',%s' % self.options

        return mark_safe(u'$(\'#%s\').autocomplete(%s%s);' % (field_id, source, options))

    def render(self, name, value=None, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value:
            final_attrs['value'] = escape(smart_unicode(value))

        if not self.attrs.has_key('id'):
            final_attrs['id'] = 'id_%s' % name

        return mark_safe(u'''<input type="text" %(attrs)s/>
        <script type="text/javascript"><!--//
        %(js)s//--></script>
        ''' % {
            'attrs': flatatt(final_attrs),
            'js': self.render_js(final_attrs['id']),
            })