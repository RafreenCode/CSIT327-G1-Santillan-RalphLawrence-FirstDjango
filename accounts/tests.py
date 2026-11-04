from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class AccountFlowTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="student", password="Campus-test-9821")

    def test_signup_shows_success_and_defaults_to_student(self):
        response = self.client.post(reverse("signup"), {
            "username": "newmember", "email": "new@example.com",
            "first_name": "New", "last_name": "Member", "course": "CS",
            "password1": "Campus-test-9821", "password2": "Campus-test-9821",
            "role": "ADMIN",
        }, follow=True)
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Your account has been created successfully")
        self.assertEqual(CustomUser.objects.get(username="newmember").role, CustomUser.Role.STUDENT)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("profile"))

    def test_profile_updates_only_current_user_without_role_changes(self):
        other = CustomUser.objects.create_user(username="other")
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile"), {
            "username": "student", "first_name": "Alex", "last_name": "Rivera",
            "email": "alex@example.com", "course": "Computer Science",
            "role": "ADMIN", "is_staff": "true", "pk": other.pk,
        }, follow=True)
        self.assertRedirects(response, reverse("profile"))
        self.assertContains(response, "Your profile has been updated successfully")
        self.user.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(self.user.first_name, "Alex")
        self.assertEqual(self.user.role, CustomUser.Role.STUDENT)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(other.first_name, "")

    def test_duplicate_username_preserves_existing_profile(self):
        CustomUser.objects.create_user(username="taken")
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile"), {"username": "taken"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "student")
