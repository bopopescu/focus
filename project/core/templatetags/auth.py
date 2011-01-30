from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.tag
def require_permission(parser, token):
    """
    Tag that only shows its content if the user has the required permission

    Usage:
        {% require_permission ACTION object %}

    Params:
        ACTION: The action to check if the user has permission to do on..
        object: The object the user can do something with

    Example:
        {% for quote in quotes %}
            {% require_permission EDIT quote %}
                ...edit link for a single quote here...
            {% end_require %}
        {% endfor %}

    Example:
        {% require_permission EDIT quote.Quote %}
            Something someone who can edit all quotes can see
        {% end_require %}

    """

    # Extract the params
    try:
        tag_name, action, object = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]

    # Fetch everything from this tag to end_require
    nodelist = parser.parse(('end_require',))
    parser.delete_first_token()

    return PermissionNode(nodelist, action, object)

class PermissionNode(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, nodelist, action, object):
        self.nodelist = nodelist
        self.action = action

        # Tries to parse a variable name to an actual variable,
        # enables us to use template variables in the tag params
        self.object = template.Variable(object)

    def render(self, context):
        # If the object param resolves into an actual object, use that to check
        # if the user has permission

        try:
            object = self.object.resolve(context)

            if context['user'].has_permission_to(self.action, object):
                return self.nodelist.render(context)
            else:
                return ''

        # Else, the object is just a string. We find the model corrosponding to that string,
        # and check if the user has permission to do something with all of those objects
        except template.VariableDoesNotExist:
            # Get the app and then the model name from app.modelname
            app, model = self.object.__str__().lower().split(".")

            content_type = ContentType.objects.get(app_label=app, model=model)
            model = content_type.model_class()

            if context['user'].has_permission_to(self.action, model):
                return self.nodelist.render(context)
            else:
                return ''