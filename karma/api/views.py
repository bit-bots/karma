from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import mixins, viewsets

from karma.api.serializers import KarmaSerializer, ProjectSerializer
from karma.karma.models import KarmaPoints, Project


class KarmaViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin):
    serializer_class = KarmaSerializer
    queryset = KarmaPoints.objects.all()


class ProjectViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(Q(user=self.request.user) | Q(group__in=self.request.user.groups.all()))
