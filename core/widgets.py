from django.template.loader import render_to_string
import django.forms as forms

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