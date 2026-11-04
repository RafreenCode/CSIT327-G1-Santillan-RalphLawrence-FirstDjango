from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser


class DashboardAccessTests(TestCase):
    def test_superuser_with_default_student_role_can_access_panel(self):
        user = CustomUser.objects.create_superuser(username="superadmin", password="Campus-test-9821")
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("admin_panel")).status_code, 200)
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, 'href="' + reverse("admin_panel") + '"')
        self.assertContains(response, "Open admin panel")

    def test_staff_status_alone_does_not_grant_panel_access(self):
        user = CustomUser.objects.create_user(username="staff", is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("admin_panel")).status_code, 403)

    def test_inactive_admin_does_not_have_panel_permission(self):
        user = CustomUser(role=CustomUser.Role.ADMIN, is_superuser=True, is_active=False)
        self.assertFalse(user.can_access_admin_panel)

    def test_anonymous_visitors_require_login(self):
        for route in ("dashboard", "admin_panel"):
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse("login")))

    def test_students_and_instructors_cannot_access_admin_panel(self):
        for role in (CustomUser.Role.STUDENT, CustomUser.Role.INSTRUCTOR):
            user = CustomUser.objects.create_user(username=role, role=role)
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse("admin_panel")).status_code, 403)
            self.assertContains(self.client.get(reverse("dashboard")), "Manage profile")

    def test_admin_sees_real_member_counts(self):
        admin = CustomUser.objects.create_user(username="admin", role=CustomUser.Role.ADMIN)
        CustomUser.objects.create_user(username="student")
        self.client.force_login(admin)
        response = self.client.get(reverse("admin_panel"))
        self.assertContains(response, "Community overview")
        self.assertEqual(response.context["member_count"], 2)
        self.assertEqual(response.context["student_count"], 1)
        self.assertEqual(response.context["admin_count"], 1)
        self.assertEqual(response.context["instructor_count"], 0)
