from django import template
from django.contrib.contenttypes.models import ContentType
from app.timetracking.helpers import validForEdit
from django.core import urlresolvers

register = template.Library()

@register.tag
def require_valid_date_for_edit(parser, token):
    """
    Tag that only shows its content if the user has the required permission

    Usage:
        {% require_valid_date_for_edit object %}

    """

    # Extract the params
    try:
        tag_name, object = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument (object)" % token.contents.split()[0]

    # Fetch everything from this tag to end_require
    nodelist = parser.parse(('end_require',))
    parser.delete_first_token()

    return DateValidForEdtNode(nodelist, object)

class DateValidForEdtNode(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, nodelist, object):
        self.nodelist = nodelist
        self.object = template.Variable(object)

    def render(self, context):
        # If the object param resolves into an actual object, use that to check
        # if the user has permission

        try:
            object = self.object.resolve(context)

            if context['user'].has_permission_to("EDIT", object) and validForEdit(object.date.strftime("%d.%m.%Y")):
                return self.nodelist.render(context)
            else:
                return ''

        except template.VariableDoesNotExist:
            return ''


@register.tag
def links_for_archived_month(parser, token):
    """

    Usage:
        {% link_for_archived_month year month %}

    """

    # Extract the params
    try:
        tag_name, year, month = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument (object)" % token.contents.split()[0]

    return linksForArchivedMonth(year, month)

class linksForArchivedMonth(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, year, month):
        self.year = template.Variable(year)
        self.month = template.Variable(month)

    def render(self, context):
        months = (self.month.resolve(context))
        year = int(self.year.resolve(context))

        try:
            string = ""

            for month in sorted(months):
                monthNames = ['Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
                          'November', 'Desember']

                string += " <a href='%s'>%s</a>" % (
                urlresolvers.reverse('app.timetracking.views.viewArchivedMonth', args=("%s" % year, "%s" % month)),
                monthNames[month - 1])

            return string

        except template.VariableDoesNotExist:
            return ''