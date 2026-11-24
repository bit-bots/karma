from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from simple_openid_connect.data import UserinfoSuccessResponse
from simple_openid_connect.integrations.django.models import OpenidUser

from karma.calibration.models import Calibration
from karma.karma.models import Category, KarmaPoints, Project
from karma.karma.openid import KarmaUserMapper


class ApplicationCompatibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("existing-user", password="test-password")
        cls.project = Project.objects.create(name="Existing project", user=cls.user)
        cls.category = Category.objects.create(name="Existing category", project=cls.project)
        cls.point = KarmaPoints.objects.create(
            user=cls.user,
            project=cls.project,
            category=cls.category,
            points=42,
            description="Existing entry",
            time=now(),
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_unauthenticated_request_redirects_to_openid(self):
        self.client.logout()
        response = self.client.get(reverse("karma_personal"))
        self.assertRedirects(
            response,
            reverse("simple_openid_connect:login") + "?next=/karma/personal",
            fetch_redirect_response=False,
        )

    def test_authenticated_pages_render(self):
        urls = [
            reverse("karma_personal"),
            reverse("karma_add_project"),
            reverse("karma_add_categories"),
            reverse("karma_project_overview", args=[self.project.pk]),
            reverse("karma_category_overview", args=[self.category.pk]),
            reverse("karma_project_user", args=[self.project.pk, self.user.username]),
            reverse("karma_project_highscore", args=[self.project.pk, 30]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_point_form_creates_and_edits_related_records(self):
        data = {
            "description": "New entry",
            "points": 15,
            "project": self.project.pk,
            "category": self.category.pk,
            "time": now().strftime("%Y-%m-%d %H:%M"),
        }
        self.assertEqual(self.client.post(reverse("karma_personal"), data).status_code, 302)
        point = KarmaPoints.objects.get(description="New entry")
        self.assertEqual(point.user_id, self.user.pk)
        data["points"] = 25
        response = self.client.post(reverse("edit_points", args=[point.pk]), data)
        self.assertEqual(response.status_code, 302)
        point.refresh_from_db()
        self.assertEqual(point.points, 25)

    def test_api_preserves_project_and_point_representation(self):
        response = self.client.get("/api/projects/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"name": self.project.name, "categories": [self.category.name]}],
        )
        response = self.client.get("/api/karma/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["user"], self.user.username)
        self.assertEqual(response.json()[0]["points"], 42)

    def test_api_aggregations_preserve_results(self):
        response = self.client.get("/api/karma/by_day/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["points__sum"], 42)
        response = self.client.get(
            "/api/highscore/",
            {"project": self.project.name, "days": 30},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {self.user.username: 42})

    def test_openid_mapper_reuses_existing_user_and_preserves_membership(self):
        group = Group.objects.create(name="Existing group")
        self.user.groups.add(group)
        data = UserinfoSuccessResponse.model_validate(
            {"sub": "existing-subject", "preferred_username": self.user.username}
        )
        mapped = KarmaUserMapper().handle_federated_userinfo(data)
        self.assertEqual(mapped.pk, self.user.pk)
        self.assertEqual(OpenidUser.objects.get(sub=data.sub).user_id, self.user.pk)
        self.assertTrue(mapped.groups.filter(pk=group.pk).exists())
        self.assertEqual(User.objects.count(), 1)

    def test_existing_primary_key_types_are_preserved(self):
        for model in (Project, Category, KarmaPoints, Calibration):
            with self.subTest(model=model.__name__):
                self.assertEqual(model._meta.pk.get_internal_type(), "AutoField")
