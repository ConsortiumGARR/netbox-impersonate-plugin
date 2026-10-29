from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from impersonate.models import ImpersonationLog

User = get_user_model()

START = "plugins:netbox_impersonate_plugin:impersonate_start"
STOP = "plugins:netbox_impersonate_plugin:impersonate_stop"


class ImpersonateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("admin1", password="x", is_superuser=True)
        cls.other_admin = User.objects.create_user(
            "admin2", password="x", is_superuser=True
        )
        cls.user = User.objects.create_user("plain", password="x")
        cls.inactive = User.objects.create_user("gone", password="x", is_active=False)

    def login(self, user):
        self.client.force_login(user)

    def whoami(self):
        return self.client.get(reverse("account:profile")).context["request"].user

    def test_start_switches_user_and_stop_restores(self):
        self.login(self.admin)
        self.client.post(reverse(START, args=[self.user.pk]))
        self.assertEqual(self.whoami(), self.user)
        self.client.post(reverse(STOP))
        self.assertEqual(self.whoami(), self.admin)

    def test_banner_only_while_impersonating(self):
        self.login(self.admin)
        self.assertNotContains(self.client.get(reverse("home")), "Impersonating")
        self.client.post(reverse(START, args=[self.user.pk]))
        self.assertContains(self.client.get(reverse("home")), "Impersonating plain")

    def test_button_on_user_page(self):
        self.login(self.admin)
        url = reverse("users:user", args=[self.user.pk])
        self.assertContains(self.client.get(url), reverse(START, args=[self.user.pk]))

    def test_button_in_user_list(self):
        self.login(self.admin)
        response = self.client.get(reverse("users:user_list"))
        self.assertContains(response, reverse(START, args=[self.user.pk]))
        self.assertNotContains(response, reverse(START, args=[self.other_admin.pk]))
        self.assertNotContains(response, reverse(START, args=[self.inactive.pk]))

    def test_non_superuser_cannot_start(self):
        self.login(self.user)
        self.client.post(reverse(START, args=[self.admin.pk]))
        self.assertFalse(ImpersonationLog.objects.exists())

    def test_cannot_impersonate_superuser_self_or_inactive(self):
        self.login(self.admin)
        for target in (self.other_admin, self.admin, self.inactive):
            self.client.post(reverse(START, args=[target.pk]))
            self.assertEqual(self.whoami(), self.admin)

    def test_cannot_switch_target_while_impersonating(self):
        self.login(self.admin)
        self.client.post(reverse(START, args=[self.user.pk]))
        other = User.objects.create_user("other", password="x")
        self.client.post(reverse(START, args=[other.pk]))
        self.assertEqual(self.whoami(), self.user)

    def test_start_and_stop_require_post(self):
        self.login(self.admin)
        self.assertEqual(
            self.client.get(reverse(START, args=[self.user.pk])).status_code, 405
        )
        self.assertEqual(self.client.get(reverse(STOP)).status_code, 405)

    def test_session_is_logged(self):
        self.login(self.admin)
        self.client.post(reverse(START, args=[self.user.pk]))
        self.client.post(reverse(STOP))
        log = ImpersonationLog.objects.get()
        self.assertEqual((log.impersonator, log.impersonating), (self.admin, self.user))
        self.assertIsNotNone(log.session_ended_at)

    def test_demoted_admin_loses_impersonation(self):
        self.login(self.admin)
        self.client.post(reverse(START, args=[self.user.pk]))
        User.objects.filter(pk=self.admin.pk).update(is_superuser=False)
        self.assertEqual(self.whoami(), self.admin)
