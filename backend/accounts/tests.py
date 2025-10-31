from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from accounts.models import Role, Resource

User = get_user_model()

class FilterOrderingTests(APITestCase):
    def setUp(self):
        # Crear rol/recursos y usuarios
        self.r_read = Resource.objects.create(key="users.read", name="Leer usuarios")
        role = Role.objects.create(name="Manager", slug="manager")
        role.resources.add(self.r_read)

        self.u1 = User.objects.create_user(username="ana", email="ana@example.com", password="pass12345")
        self.u2 = User.objects.create_user(username="beto", email="beto@example.com", password="pass12345")
        self.u1.roles.add(role); self.u2.roles.add(role)

        # Autenticar vía sesión (bypaséando login view para test)
        self.client = APIClient()
        self.client.force_login(self.u1)

    def test_search_and_order(self):
        url = "/api/v1/users/?search=et&ordering=-username"
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        usernames = [u["username"] for u in r.data["results"]]
        self.assertTrue("beto" in usernames or "ana" in usernames)

    def test_filter_by_role_slug(self):
        url = "/api/v1/users/?roles__slug=manager"
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.data["count"], 2)
