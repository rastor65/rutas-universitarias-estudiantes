from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import Role, Resource, Permission


@receiver(post_migrate)
def init_roles_resources(sender, **kwargs):
    """
    Crea automáticamente los roles, recursos y permisos base
    después de ejecutar migrate o al iniciar el servidor.
    """
    if sender.name != "accounts":
        return

    print("\n⚙️  Inicializando roles, recursos y permisos base...")

    # === PERMISOS BASE ===
    permisos_base = [
        ("view", "Visualizar recurso"),
        ("add", "Crear recurso"),
        ("edit", "Editar recurso"),
        ("delete", "Eliminar recurso"),
    ]

    for code, name in permisos_base:
        Permission.objects.get_or_create(
            code=code,
            defaults={"name": name, "description": f"Permite {name.lower()}."},
        )

    permisos = list(Permission.objects.all())

    # === RECURSOS BASE ===
    recursos_base = [
        ("usuarios", "Gestión de usuarios", "/api/accounts/users/", "user"),
        ("roles", "Gestión de roles", "/api/accounts/roles/", "roles"),
        ("permisos", "Gestión de permisos", "/api/accounts/permissions/", "permissions"),
        ("rutas", "Gestión de rutas", "/api/rutas/", "routes"),
        ("paradas", "Gestión de paradas", "/api/paradas/", "stops"),
        ("cupos", "Gestión de cupos", "/api/cupos/", "slots"),
        ("gps", "Monitoreo GPS", "/api/gps/", "gps"),
    ]

    recursos_creados = []
    for nombre, descripcion, link, icono in recursos_base:
        recurso, created = Resource.objects.get_or_create(
            name=nombre,
            defaults={
                "description": descripcion,
                "link_backend": link,
                "icon": icono,
            },
        )
        # Asignar todos los permisos base a cada recurso
        recurso.permissions.set(permisos)
        recursos_creados.append(recurso)

    # === ROLES BASE ===
    roles_base = [
        ("Administrador", "admin", "Acceso total a todas las operaciones del sistema."),
        ("Conductor", "conductor", "Acceso a rutas asignadas, posiciones GPS y llenados."),
        ("Estudiante", "estudiante", "Puede reservar cupos y consultar rutas disponibles."),
        ("Coordinador", "coordinador", "Gestión de asignaciones y validación de reportes."),
    ]

    for nombre, slug, descripcion in roles_base:
        Role.objects.get_or_create(
            slug=slug,
            defaults={"name": nombre, "description": descripcion},
        )

    # === ASIGNACIÓN DE RECURSOS A ROLES ===
    admin = Role.objects.filter(slug="admin").first()
    conductor = Role.objects.filter(slug="conductor").first()
    estudiante = Role.objects.filter(slug="estudiante").first()
    coordinador = Role.objects.filter(slug="coordinador").first()

    if admin:
        admin.resources.set(Resource.objects.all())

    if conductor:
        conductor.resources.set(
            Resource.objects.filter(name__in=["rutas", "gps"])
        )

    if estudiante:
        estudiante.resources.set(
            Resource.objects.filter(name__in=["rutas", "cupos", "paradas"])
        )

    if coordinador:
        coordinador.resources.set(
            Resource.objects.filter(name__in=["rutas", "roles", "usuarios"])
        )

    print("✅ Roles, recursos y permisos base inicializados correctamente.\n")




from django.contrib.auth.signals import user_logged_in, user_logged_out
from accounts.models import UserActivityLog

@receiver(user_logged_in)
def registrar_login(sender, user, request, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="auth.login",
        description="Inicio de sesión exitoso",
        ip_address=getattr(request, "client_ip", None),
        device=getattr(request, "user_agent", None),
    )


@receiver(user_logged_out)
def registrar_logout(sender, user, request, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="auth.logout",
        description="Cierre de sesión",
        ip_address=getattr(request, "client_ip", None),
        device=getattr(request, "user_agent", None),
    )
