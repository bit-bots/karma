from rest_framework import mixins, viewsets

from karma.api.serializers import KarmaSerializer
from karma.karma.models import KarmaPoints


class KarmaViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin):
    serializer_class = KarmaSerializer
    queryset = KarmaPoints.objects.all()
