from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from karma.karma.models import KarmaPoints, Project, Category


class KarmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaPoints
        fields = ('user', 'time', 'points', 'description', 'project', 'category')

    user = serializers.ReadOnlyField(source='user.username')
    project = serializers.CharField(source='project.name')
    category = serializers.CharField(source='category.name')

    def validate(self, attrs):
        try:
            attrs['project'] = Project.objects.get(name=attrs['project']['name'])
        except ObjectDoesNotExist:
            raise ValidationError('Project does not exist')
        try:
            attrs['category'] = Category.objects.get(name=attrs['category']['name'], project=attrs['project'])
        except ObjectDoesNotExist:
            raise ValidationError('Category does not exist')
        attrs['user'] = self.context['request'].user
        user_is_owner = attrs['user'] == attrs['project'].user
        user_in_project_group = attrs['project'].group is not None and attrs['user'].groups.filter(
            name=attrs['project'].group.name).exists()
        if not (user_is_owner or user_in_project_group):
            raise ValidationError('Project does not exist')
        return attrs


class CategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'categories')

    categories = CategoryField(many=True, read_only=True)


class HighscoreSerializer(serializers.Serializer):
    def to_representation(self, instance: QuerySet):
        return instance.values_list('user__username', 'points')

    def validate(self, attrs):
        print(attrs)
        return attrs
