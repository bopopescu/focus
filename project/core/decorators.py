import functools
from django.http import Http404
from django.core import urlresolvers
from django.shortcuts import redirect

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

    Params:
        action: The action the user has to have permission to do
        model: The model we want to check that the user is allowed to do action on
        field (optional): The field in the URL in which we can find the primary key identifiying this instance of the model
                          If left blank, you're checking if the user is allowed to do something with ALL objects
                          of this kind. Typically this value will be "id"
        field_db (optional): The the primary key field in the model corrosponding to the field in the URL.
                             If left blank, it's copied from "field".
        any (optional):

    """

    action = None
    model = None
    field = None
    field_db = None
    any = False

    def __init__(self, action, model, field=False, field_db=False, any=False):
        """
        Used for decorator permission checking
        Called when python finds a decorator
        """

        self.action = action
        self.model = model
        self.any = any

        # First, we automaticly presume the field in the db is named the same as the field
        if field:
            self.field = field
            self.field_db = field

        # Then we change it, if it's not
        if field_db:
            if not field:
                raise Exception(
                        "A database field was defined without a corrosponding view function field. See core.require_permission for more info")

            self.field_db = field_db

    def __call__(self, func):
        """
        Used for decorator permission checking
        Called when a method we have decorated is called
        """

        def check_permission (request, *args, **kwargs):
            # If the identifier is defined, get the object instance
            if self.field:
                if not self.field in kwargs:
                    print "KWARGS: %s" % kwargs
                    raise Exception(
                            "The specified field '%s' in the require_permission decorator did not match a input argument." % self.field)

                # Get the object instance, or 404 if it does not exist
                try:
                    object = self.get_object(kwargs)

                except self.model.DoesNotExist:
                    raise Http404()

            # Otherwise, just use the model class itself
            else:
                object = self.model

            if not request.user:
                return redirect("/accounts/login/?next=%s" % (request.path))

            # If the user has permission to use this view, go ahead and use it! :)
            if request.user.has_permission_to(self.action, object, any=any):
                return func(request, *args, **kwargs)

            # Else, if the user isn't logged in, suggest doing so
            elif not request.user.logged_in():
                return redirect("/accounts/login/?next=%s" % (request.path))

            # Else, we just have to tell the user he just can't do this
            else:
                request.message_error("Ingen tilgang")
                return redirect(urlresolvers.reverse('app.dashboard.views.overview'))

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
        object = self.model.objects.get(**query)

        return object