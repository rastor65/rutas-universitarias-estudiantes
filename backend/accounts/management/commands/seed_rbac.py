from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role, Resource

User = get_user_model()

RESOURCES = [
    ("auth.password.change", "Cambiar contraseña"),
    ("users.read", "Ver usuarios"),
    ("users.write", "Gestionar usuarios"),
    ("roles.read", "Ver roles"),
    ("roles.write", "Gestionar roles"),
    ("resources.read", "Ver recursos"),
    ("resources.write", "Gestionar recursos"),
]

ROLES = {
    "admin": ["auth.password.change","users.read","users.write","roles.read","roles.write","resources.read","resources.write"],
    "manager": ["users.read","roles.read","resources.read","auth.password.change"],
    "staff": ["auth.password.change"],
}

class Command(BaseCommand):
    help = "Crea recursos, roles y un superusuario demo"

    def handle(self, *args, **options):
        # Recursos
        for key, name in RESOURCES:
            Resource.objects.get_or_create(key=key, defaults={"name": name})

        # Roles + asignación de recursos
        for role_name, keys in ROLES.items():
            role, _ = Role.objects.get_or_create(
                slug=role_name, defaults={"name": role_name.capitalize()}
            )
            resources = list(Resource.objects.filter(key__in=keys))
            role.resources.set(resources)

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin12345"
            )
            admin_role = Role.objects.get(slug="admin")
            admin.roles.add(admin_role)
            self.stdout.write(self.style.SUCCESS("Superusuario admin/admin12345 creado y rol admin asignado."))
        else:
            self.stdout.write("Superusuario admin ya existe.")

        self.stdout.write(self.style.SUCCESS("Seed RBAC completado."))
