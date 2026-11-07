from django.test import Client, TestCase
from django.urls import reverse
from django.views.generic import UpdateView
from .views import ProfileUpdateView
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
        self.assertContains(response, "alert-success")
        self.assertContains(response, 'role="status"')
        self.assertNotContains(self.client.get(reverse("login")), "Your account has been created successfully")
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


    def test_lab_forms_share_bootstrap_styling(self):
        for route in ("signup", "login", "profile"):
            if route == "profile":
                self.client.force_login(self.user)
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "base.html")
            self.assertContains(response, "bootstrap@5.3.3/dist/css/bootstrap.min.css")
            self.assertContains(response, 'class="form-control"')
            self.assertContains(response, 'class="form-label"')
            self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_profile_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(reverse("profile"), {"username": "changed"})
        self.assertEqual(response.status_code, 403)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "student")


    def test_profile_is_updateview_and_ignores_other_user_query(self):
        self.assertTrue(issubclass(ProfileUpdateView, UpdateView))
        other = CustomUser.objects.create_user(username="private-other", first_name="Private")
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"), {"pk": other.pk, "user_id": other.pk})
        self.assertEqual(response.context["object"].pk, self.user.pk)
        self.assertNotContains(response, 'value="Private"')
        self.assertEqual(self.client.get(f"/accounts/profile/{other.pk}/").status_code, 404)

    def test_invalid_signup_does_not_show_success_or_create_user(self):
        response = self.client.post(reverse("signup"), {
            "username": "invalid-user", "password1": "Campus-test-9821",
            "password2": "different-password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotContains(response, "Your account has been created successfully")
        self.assertFalse(CustomUser.objects.filter(username="invalid-user").exists())

    def test_real_login_profile_save_and_logout_with_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("login"))
        response = client.post(reverse("login"), {
            "username": "student", "password": "Campus-test-9821",
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        }, follow=True)
        self.assertRedirects(response, reverse("dashboard"))
        client.get(reverse("profile"))
        response = client.post(reverse("profile"), {
            "username": "student", "first_name": "Verified", "last_name": "Student",
            "email": "verified@example.com", "course": "Computer Science",
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        }, follow=True)
        self.assertRedirects(response, reverse("profile"))
        self.assertContains(response, "alert-success")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Verified")
        self.assertContains(client.get(reverse("profile")), 'value="Verified"')
        response = client.post(reverse("logout"), {
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        }, follow=True)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(client.get(reverse("profile")).status_code, 302)

    def test_signup_and_login_reject_posts_without_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for route in ("signup", "login"):
            self.assertEqual(client.post(reverse(route), {}).status_code, 403)

    def test_django_admin_pages_load(self):
        self.assertEqual(self.client.get(reverse("admin:login")).status_code, 200)
        admin = CustomUser.objects.create_superuser(username="page-admin", password="Campus-test-9821")
        self.client.force_login(admin)
        for route in ("admin:index", "admin:accounts_customuser_changelist", "admin:accounts_customuser_add"):
            self.assertEqual(self.client.get(reverse(route)).status_code, 200)
