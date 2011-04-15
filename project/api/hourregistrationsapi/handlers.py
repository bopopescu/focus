from piston.handler import BaseHandler
from piston.utils import rc
from app.hourregistrations.models import HourRegistration
from core import Core

class HourRegistrationHandler(BaseHandler):
    model = HourRegistration
    allowed_methods = ('GET', 'PUT', 'POST')
    fields = ('date', ('order', ('id', 'order_name')), ('typeOfWork', ('name', )), 'time_start', 'time_end', 'description',
              'pause', 'hours_worked', )


    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", HourRegistration).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except HourRegistration.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request):
        pass

    def update(self, request, id):
        pass



    
