from app.projects.models import Project
from piston.handler import BaseHandler
from piston.utils import rc
from core import Core
from django.core import urlresolvers
from core.auth.user.models import User

class ProjectHandler(BaseHandler):
    model = Project
    fields = ('id', 'project_name', ('files', ('id','get_file')))

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Project)
        if id:
            try:
                return all.get(id=id)
            except Project.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

