from rest_framework import viewsets

from ado.apps.routes.models import Route
from ado.apps.routes.api.serializers import RouteSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().order_by('pk')
    serializer_class = RouteSerializer
