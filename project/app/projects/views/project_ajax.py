from app.customers.models import Customer
from app.projects.models import Project
from app.projects.forms import ProjectForm, ProjectFormSimple
from core.decorators import require_permission
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core import serializers

@require_permission("CREATE", Project)
def add(request):
    form = ProjectFormSimple(request.POST, instance=Project())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.project_name,
                                              'id': a.id,
                                              'valid': True}), mimetype='application/json')

    else:
        errors = dict([(field, errors[0]) for field, errors in form.errors.items()])

        return HttpResponse(simplejson.dumps({'errors': errors,
                                              'valid': False}), mimetype='application/json')

    return HttpResponse("ERROR")


def list_by_customer(request):

    customerID = request.GET['id']

    json_serializer = serializers.get_serializer("json")()

    projects = Project.objects.filter(customer = Customer.objects.get(id=customerID))

    return HttpResponse(serializers.serialize('json', projects))

    """
    return HttpResponse(simplejson.dumps({'projects': projects,
                                          }), mimetype='application/json')
    """