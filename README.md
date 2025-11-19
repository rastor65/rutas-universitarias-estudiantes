# 🚌 Rutas Universitarias - API Backend

Sistema de gestión de rutas universitarias con autenticación, control de cupos, monitoreo GPS y paradas de autobús.

## 📋 Descripción General

API REST desarrollada con **Django Rest Framework** que permite:
- ✅ Autenticación y autorización basada en roles (RBAC)
- ✅ Gestión de rutas de autobús
- ✅ Control de cupos disponibles
- ✅ Monitoreo GPS en tiempo real
- ✅ Administración de paradas
- ✅ **Sistema de auditoría completo**
- ✅ **Middleware de captura de información de requests**
- ✅ **Dockerización con MySQL**
- ✅ **Sistema de logs de actividad de usuarios**

### Stack Tecnológico

| Componente | Versión |
|---|---|
| Python | 3.13+ |
| Django | 5.2.8 |
| Django REST Framework | 3.16.1 |
| PostgreSQL / SQLite / MySQL | - |
| JWT | simplejwt 5.5.1 |
| CORS | django-cors-headers 4.9.0 |
| Docker | 24.0+ |
| MySQL | 8.0 |

---

## 🚀 Instalación Rápida

### Opción 1: Docker (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/Stirven0/rutas-universitarias-estudiantes.git
cd rutas-universitarias-estudiantes

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar con Docker Compose
docker-compose up -d

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Cargar datos iniciales RBAC
docker-compose exec web python manage.py seed_rbac
```

### Opción 2: Instalación tradicional

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd rutas-universitarias-estudiantes

# 2. Crear entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Cargar datos iniciales (RBAC)
python manage.py seed_rbac

# 8. Ejecutar servidor
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

---

## 📁 Estructura del Proyecto Actualizada

```
rutas-universitarias-estudiantes/
├── .env                              # Variables de entorno
├── .env.example                      # Plantilla de variables
├── .gitignore                        # Archivos ignorados por git
├── .dockerignore                     # Archivos ignorados por Docker
├── README.md                         # Documentación del proyecto
├── requirements.txt                  # Dependencias Python
├── Dockerfile                        # Imagen Docker
├── docker-compose.yml                # Orquestación Docker
│
└── backend/
    ├── manage.py                     # Script de gestión Django
    ├── db.sqlite3                    # BD SQLite (desarrollo)
    ├── rutas_universitarias.sqlite3  # BD alternativa SQLite
    ├── .env.example                  # Plantilla variables (en backend)
    │
    ├── backend/                      # Configuración principal
    │   ├── __init__.py
    │   ├── settings.py               # Configuración Django
    │   ├── urls.py                   # Rutas principales
    │   ├── asgi.py                   # ASGI (async)
    │   └── wsgi.py                   # WSGI (producción)
    │
    ├── accounts/                     # Autenticación y RBAC
    │   ├── __init__.py
    │   ├── admin.py                  # Admin Django
    │   ├── apps.py                   # Config app
    │   ├── models.py                 # User, Role, Resource, UserActivityLog
    │   ├── views.py                  # Vistas autenticación
    │   ├── serializers.py            # Serializadores
    │   ├── urls.py                   # Rutas /api/accounts/
    │   ├── permissions.py            # Permisos personalizados (RBAC)
    │   ├── middleware.py             # Middleware (CaptureRequestInfoMiddleware)
    │   ├── audit.py                  # Auditoría y logging
    │   ├── signals.py                # Señales Django
    │   ├── exceptions.py             # Excepciones custom
    │   ├── tests.py                  # Tests unitarios
    │   └── management/
    │       └── commands/
    │           └── seed_rbac.py      # Comando cargar RBAC
    │
    ├── rutas/                        # Gestión de rutas y buses
    │   ├── __init__.py
    │   ├── admin.py                  # Admin Django
    │   ├── apps.py                   # Config app
    │   ├── models.py                 # Ruta, Bus
    │   ├── serializer.py             # Serializadores
    │   ├── views.py                  # ViewSets
    │   ├── urls.py                   # Rutas /api/rutas/
    │   └── tests.py                  # Tests
    │
    ├── gps/                          # Monitoreo GPS
    │   ├── __init__.py
    │   ├── admin.py                  # Admin Django
    │   ├── apps.py                   # Config app
    │   ├── models.py                 # GPSPosicion, EventoDesvio
    │   ├── serializers.py            # Serializadores
    │   ├── views.py                  # ViewSets GPS
    │   ├── urls.py                   # Rutas /api/gps/
    │   └── tests.py                  # Tests
    │
    ├── gestion_cupo/                 # Control de cupos
    │   ├── __init__.py
    │   ├── admin.py                  # Admin Django
    │   ├── apps.py                   # Config app
    │   ├── models.py                 # Cupo
    │   ├── serializers.py            # Serializadores
    │   ├── views.py                  # ViewSets cupos
    │   ├── urls.py                   # Rutas /api/cupos/
    │   └── tests.py                  # Tests
    │
    └── paradas/                      # Administración de paradas
        ├── __init__.py
        ├── admin.py                  # Admin Django
        ├── apps.py                   # Config app
        ├── models.py                 # Parada
        ├── serializers.py            # Serializadores
        ├── views.py                  # ViewSets paradas
        ├── urls.py                   # Rutas /api/paradas/
        └── tests.py                  # Tests
```

---

## ⚙️ Configuración de Variables de Entorno

### Variables Críticas

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta (debe ser aleatoria en producción) | `django-insecure-...` |
| `DJANGO_DEBUG` | Modo debug (False en producción) | `True` / `False` |
| `DB_ENGINE` | Tipo de base de datos | `sqlite` / `postgres` / `mysql` |
| `EMAIL_HOST_PASSWORD` | Contraseña de email (App Password si es Gmail) | `wnbfflevmkkjnnlv` |

### Configuración para MySQL (Docker)

```env
DB_ENGINE=mysql
DB_NAME=rutas_universitarias
DB_USER=root
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=3306
```

### Configuración para PostgreSQL

```env
DB_ENGINE=postgres
DB_NAME=rutas_universitarias
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=localhost
DB_PORT=5432
```

### Configuración para Gmail (2FA)

1. Habilita 2FA en tu cuenta de Google
2. Genera una **App Password** en: https://myaccount.google.com/apppasswords
3. Copia la contraseña generada en `EMAIL_HOST_PASSWORD`

---

## 🐳 Docker Configuration

### Servicios Disponibles

| Servicio | Puerto | Descripción |
|---|---|---|
| `web` (Django) | 8000 | API Backend principal |
| `db` (MySQL) | 3307 | Base de datos MySQL |

### Comandos Docker Útiles

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f web

# Detener servicios
docker-compose down

# Ejecutar comandos en el contenedor
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Backup de base de datos
docker-compose exec db mysqldump -u root -p1234 rutas_universitarias > backup.sql
```

---

## 🔐 Autenticación y Seguridad Mejorada

### JWT (Token)

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "contraseña"
  }'

# 2. Usar token en requests
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/users/
```

### Sistema de Auditoría

- **Logs de actividad**: Todos los requests se registran automáticamente
- **Middleware de captura**: Información detallada de cada petición
- **RBAC avanzado**: Control de permisos por roles y recursos

---

## 📚 Endpoints Principales

### Autenticación

```
POST   /api/auth/login/          - Iniciar sesión
POST   /api/auth/logout/         - Cerrar sesión
POST   /api/auth/token/          - Obtener token JWT
POST   /api/auth/refresh/        - Refrescar token
POST   /api/password-reset/      - Solicitar reset
```

### Usuarios

```
GET    /api/users/               - Listar usuarios
POST   /api/users/               - Crear usuario
GET    /api/users/{id}/          - Detalle usuario
PUT    /api/users/{id}/          - Actualizar usuario
DELETE /api/users/{id}/          - Eliminar usuario
```

### Rutas

```
GET    /api/rutas/               - Listar rutas
POST   /api/rutas/               - Crear ruta
GET    /api/rutas/{id}/          - Detalle ruta
PUT    /api/rutas/{id}/          - Actualizar ruta
```

### GPS

```
GET    /api/gps/posiciones/      - Historial de posiciones
POST   /api/gps/posiciones/      - Registrar posición
GET    /api/gps/desviaciones/    - Eventos de desviación
```

### Paradas

```
GET    /api/paradas/             - Listar paradas
POST   /api/paradas/             - Crear parada
GET    /api/paradas/{id}/        - Detalle parada
```

### Auditoría

```
GET    /api/audit/logs/          - Logs de actividad de usuarios
```

---

## 🛠️ Herramientas Útiles

### Admin Django
Accede a: `http://localhost:8000/admin`

- Usuarios: `http://localhost:8000/admin/accounts/user/`
- Rutas: `http://localhost:8000/admin/rutas/ruta/`
- Paradas: `http://localhost:8000/admin/paradas/parada/`
- Logs de actividad: `http://localhost:8000/admin/accounts/useractivitylog/`

### Documentación API (Swagger)
Accede a: `http://localhost:8000/api/schema/swagger/`

### Shell Django

```bash
# Traditional
python manage.py shell

# Docker
docker-compose exec web python manage.py shell
```

---

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'django'`

```bash
# Asegúrate de activar el entorno virtual
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate

pip install -r requirements.txt
```

### Error: `No such table`

```bash
python manage.py migrate
```

### Error CORS: `Access to XMLHttpRequest blocked`

Verifica que `CORS_ALLOWED_ORIGINS` en `.env` incluya tu dominio frontend.

### Puerto 8000 en uso

```bash
python manage.py runserver 8001
```

### Problemas con Docker

```bash
# Reconstruir imágenes
docker-compose build --no-cache

# Limpiar contenedores y volúmenes
docker-compose down -v

# Verificar logs
docker-compose logs web
```

---

## 📦 Dependencias Principales

Ver archivo `requirements.txt`:

- Django 5.2.8+
- djangorestframework 3.16.1+
- django-cors-headers 4.9.0+
- djangorestframework-simplejwt 5.5.1+
- drf-spectacular 0.29.0+ (API Schema)
- django-filter 25.2+
- mysqlclient 2.2.7+ (MySQL)
- psycopg2-binary 2.9.11+ (PostgreSQL)
- python-dotenv 1.2.1+

---

## 🚨 Seguridad (Producción)

### Checklist antes de desplegar

```bash
# 1. Cambiar SECRET_KEY
DJANGO_SECRET_KEY=<valor-aleatorio-seguro>

# 2. Desactivar DEBUG
DJANGO_DEBUG=False

# 3. Configurar ALLOWED_HOSTS
DJANGO_ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# 4. Usar PostgreSQL o MySQL
DB_ENGINE=postgres

# 5. Ejecutar collectstatic
python manage.py collectstatic

# 6. Cambiar claves de email
EMAIL_HOST_PASSWORD=<contraseña-real>

# 7. Verificar CORS_ALLOWED_ORIGINS

# 8. Configurar SSL/HTTPS

# 9. Revisar logs de auditoría
```

---

## 📖 Documentación Adicional

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [JWT simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Docker Django Deployment](https://docs.docker.com/samples/django/)

---

## 👥 Contribuidores

- Estudiantes de ING de Software B-2025

---

## 📄 Licencia

Este proyecto es propietario de la Universidad de La Guajira.

---

**Última actualización:** 11 de noviembre de 2025