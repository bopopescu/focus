import datetime
from haystack.indexes import *
from haystack import site

from app.projects.models import *

class ProjectIndex(SearchIndex):
    project_name = CharField(document=True, use_template=True)

site.register(Project, ProjectIndex)