from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.conf import settings
from django.db import DatabaseError

from mysqlapi.api.models import DatabaseManager


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    db = DatabaseManager(request.POST["appname"])
    try:
        db.create()
        db.create_user()
    except DatabaseError, e:
        return HttpResponse(e[1], status=500)
    config = {
        "MYSQL_DATABASE_NAME": db.name,
        "MYSQL_USER": db.name,
        "MYSQL_PASSWORD": db.password,
        "MYSQL_HOST": settings.DATABASES["default"]["HOST"],
        "MYSQL_PORT": db.port,
    }
    return HttpResponse(simplejson.dumps(config), status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def drop(request, appname):
    db = DatabaseManager(appname)
    try:
        db.drop()
        db.drop_user()
    except DatabaseError, e:
        return HttpResponse(e[1], status=500)
    return HttpResponse("", status=200)
