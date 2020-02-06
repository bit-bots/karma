from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
from django.utils.timezone import now
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from karma.api.serializers import KarmaSerializer, ProjectSerializer, HighscoreSerializer
from karma.karma.models import KarmaPoints, Project


class KarmaViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin):
    serializer_class = KarmaSerializer

    def get_queryset(self):
        return KarmaPoints.objects.filter(Q(project__user=self.request.user) | Q(project__group__in=self.request.user.groups.all()))


class ProjectViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(Q(user=self.request.user) | Q(group__in=self.request.user.groups.all()))


class HighscoreViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin):
    serializer_class = HighscoreSerializer

    def list(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(Q(name=self.request.query_params['project']) & (
                    Q(user=self.request.user) | Q(group__in=self.request.user.groups.all())))
        except ObjectDoesNotExist:
            return Response({'project': ['Project does not exist']}, status=HTTP_400_BAD_REQUEST)
        days = self.request.query_params['days']
        try:
            days = int(days)
        except ValueError:
            return Response({'days': ['Days must be a number']})

        userpoints = KarmaPoints.objects. \
            filter(project=project, time__gte=now() - timedelta(days=days)). \
            values('user__username'). \
            annotate(points=Sum('points')). \
            order_by('-points')

        serializer = self.get_serializer(userpoints)
        return Response(serializer.data)
