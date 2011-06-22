import functools, inspect, copy
from django.http import Http404
from django.core import urlresolvers
from django.shortcuts import redirect, render
from django.conf import settings

def permission_denied (request, permission_info=None):
    return render(request, 'permission_denied.html', permission_info)

class login_required:
    def __init__(self):
        pass

    def __call__(self, func):
        def check_login (request, *args, **kwargs):
            if not request.user:
                return redirect("/accounts/login/?next=%s" % (request.path))
            return func(request, *args, **kwargs)

        functools.update_wrapper(check_login, func)
        return check_login


class require_permission:
    """
    Decorator used for view authorization

    Usage:
        @require_permission("EDIT", Quote)
        def view_function_to_protect (request, ...)
            Only users who can edit all quotes can see this view

        @require_permission("EDIT", Quote, 'id')
        def view_function_to_protect (request, id, ...)
            Only users who can edit the view with the primary key from "id"
            can see this view

        @require_permission("EDIT", Quote, any = True)
        def view_function_to_protect (request, id, ...)
            Only users who can edit at least one Quote can see this view

        @require_permission("EDIT", User, field = "un", field_db = "username")
        def view_function_to_protect (request, id, ...)
            The parameter the decorator should check in the view function is called "un".
            The field in the database it should check against is called "username"
            Use this when you don't want to check against the primary key.

    Params:
        action: The action the user has to have permission to do
        model: The model we want to check that the user is allowed to do action on
        field (optional): The field in the URL in which we can find the primary key identifiying this instance of the model
                          If left blank, you're checking if the user is allowed to do something with ALL objects
                          of this kind. Typically this value will be "id"
        field_db (optional): The primary key field in the model corrosponding to the field in the URL.
                             If left blank, it's copied from "field".
        any (optional):   Return true from this function if user has permission to edit ANY of this model.
        check_deleted (optional): Will also regard objects that are deleted, instead of giving a 404

    """

    action = None
    model = None
    field = None
    field_db = None
    any = False
    check_deleted = False

    def __init__(self, action, model, field = False, field_db = False, any = False, check_deleted = False):
        """
        Used for decorator permission checking
        Called when python finds a decorator
        """

        self.action = action
        self.model = model
        self.any = any
        self.check_deleted = check_deleted

        # First, we automaticly presume the field in the db is named the same as the field
        if field:
            self.field = field
            self.field_db = field

        # Then we change it, if it's not
        if field_db:
            if not field:
                raise Exception("A database field was defined without a corrosponding view function field. See core.require_permission for more info")

            self.field_db = field_db

    def __call__(self, func):
        """
        Used for decorator permission checking
        Called when a method we have decorated is called
        """

        def check_permission (request, *args, **kwargs):

            # Put all the args in the kwargs that we search to find the object, later
            # this involves getting the argument name from the function, then putting in the values from the *args
            object_kwargs = copy.deepcopy(kwargs)

            argnames = inspect.getargspec(func).args
            for i, arg in enumerate(args):
                object_kwargs[argnames[i+1]] = arg

            # If the identifier is defined, get the object instance
            if self.field:
                if not self.field in object_kwargs:
                    raise Exception("The specified field '%s' in the require_permission decorator did not match a input argument." % self.field)

                # Get the object instance, or 404 if it does not exist
                try:
                    object = self.get_object(object_kwargs)

                except self.model.DoesNotExist:
                    if settings.DEBUG:
                        raise Exception("The object sent to @require_permission does not exist!")
                    else:
                        raise Http404()

            # Otherwise, just use the model class itself
            else:
                object = self.model

            # If the user has permission to use this view, go ahead and use it! :)
            if request.user.has_permission_to(self.action, object, any = self.any):
                return func(request, *args, **kwargs)

            # Else, if the user isn't logged in, suggest doing so
            elif not request.user.logged_in():
                return redirect("/user/login/?next=%s" % (request.path))

            # Else, we just have to tell the user he just can't do this
            else:
                return permission_denied(request, {'action': self.action,
                                                         'model': "%s.%s"  % (self.model.__module__, self.model.__name__),
                                                         'field': self.field,
                                                         'field_db': self.field_db,
                                                         'any': self.any
                                                         })

        # Update the function so it still reports correct to inspect and pydoc
        functools.update_wrapper(check_permission, func)

        # Add some info about us to the function, so other decorators can use this
        # If more decorators want to add info, generalize this! (with a decorator?)
        check_permission.__decorators__ = {'require_permission': self}

        return check_permission

    def get_object (self, kwargs):
        """
        Gets the object we're checking if the user has permission to do something with
        Override this to change how the decorator finds the object.
        """

        query = {self.field_db: kwargs[self.field]}

        if self.check_deleted:
            object = self.model.all_objects.get(**query)
        else:
            object = self.model.objects.get(**query)

        return object