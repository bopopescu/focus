
from app.customers.models import Customer
from app.projects.models import Project
from django.http import HttpResponse
from app.contacts.models import Contact
from core.shortcuts import render_with_request

def search(request):

    term = request.GET.get('s')

    searchIn = {}

    searchIn[Customer] = ["full_name",'email','address','phone']
    searchIn[Project]  = ["project_name",'pid','responsible__first_name']
    searchIn[Contact]  = ["full_name","email",'address']

    result = {}

    for o in searchIn.keys():
        for i in searchIn[o]:
            kwargs = {'%s__%s' % ('%s'%i, 'contains'): '%s'%term}
            k = o.all_objects.filter(**kwargs)
            
            for s in k:
               if s in result:
                   result[s]+=1
               else:
                   result[s]=1

    result = sorted(result.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    v = []
    for i in result:
        v.append(i[0])

    return render_with_request(request, 'search/list.html', {'title':'Resultat',
                                                                'objects':v})
    