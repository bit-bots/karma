from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from simple_openid_connect.integrations.django.models import OpenidUser
from simple_openid_connect.integrations.django.user_mapping import UserMapper


class KarmaUserMapper(UserMapper):
    def handle_federated_userinfo(self, user_data):
        # if there is already a user with this username, we create the openid association if it does not exist yet
        User = get_user_model()
        try:
            user = User.objects.get(username=user_data.preferred_username)
            OpenidUser.objects.get_or_create(
                sub=user_data.sub,
                defaults={
                    "user": user,
                },
            )
        except User.DoesNotExist:
            # if the user does not exist, it is automatically created by the super class
            pass
        return super().handle_federated_userinfo(user_data)

    def automap_user_attrs(self, user, user_data):
        super().automap_user_attrs(user, user_data)
        groups = getattr(user_data, "groups", [])
        for group_name in groups:
            group = Group.objects.get_or_create(name=group_name)[0]
            group.user_set.add(user)
            group.save()
