from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from core import Core

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
    multiple_nodes = [parser.parse(('else', 'end_require',)), None]
    token = parser.next_token()
    if token.contents == 'else':
        multiple_nodes[1] = parser.parse(('end_require',))
        parser.delete_first_token()


    return PermissionNode(multiple_nodes, action, object)

class PermissionNode(template.Node):
    """
    Node for require_permission tag
    """
    
    def __init__(self, multiple_nodes, action, object):
        self.multiple_nodes = multiple_nodes
        self.action = action
        
        # Tries to parse a variable name to an actual variable,
        # enables us to use template variables in the tag params
        self.object = template.Variable(object)
        
    def render(self, context):
        # If the object param resolves into an actual object, use that to check
        # if the user has permission
        
        try:
            object = self.object.resolve(context)

            if object is not None and context['user'].has_permission_to(self.action, object):
                return self.multiple_nodes[0].render(context)
            else:
                if self.multiple_nodes[1]:
                    return self.multiple_nodes[1].render(context)
                else:
                    return ''

        # Else, the object is just a string. We find the model corrosponding to that string,
        # and check if the user has permission to do something with all of those objects
        except template.VariableDoesNotExist:

        
            # Make a function that's cached
            def get_content_type(app, model):
                cache_key = "%s_%s" % (app, model.__class__.__name__)
                cache_key = cache_key.replace(' ','')

                if cache.get(cache_key):
                    return cache.get(cache_key)
                else:
                    result = ContentType.objects.get(app_label = app, model = model)
                    cache.set(cache_key, result)
                    return result
            
            if not 'user' in context:
                return ''
            
            # Get the app and then the model name from app.modelname
            try:
                app, model = self.object.__str__().lower().split(".")
            except ValueError:
                raise Exception ("@require_permission could not resolve object %s. " % self.object.__str__() +
                                 "Are you sure it is passed to the template? If you are checking a global permission, " +
                                 "remember to apply the appname first, like so: app.Model, e.g. quote.Quote or core.User")
                
            content_type = get_content_type(app, model)
            model = content_type.model_class()
            
            if context['user'].has_permission_to(self.action, model):
                return self.multiple_nodes[0].render(context)
            else:
                if self.multiple_nodes[1]:
                    return self.multiple_nodes[1].render(context)
                else:
                    return ''

    