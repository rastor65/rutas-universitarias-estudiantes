# 🚌 Rutas Universitarias - API Backend

Sistema de gestión de rutas universitarias con autenticación, control de cupos, monitoreo GPS y paradas de autobús.

## 📋 Descripción General

API REST desarrollada con **Django Rest Framework** que permite:
- ✅ Autenticación y autorización basada en roles (RBAC)
- ✅ Gestión de rutas de autobús
- ✅ Control de cupos disponibles
- ✅ Monitoreo GPS en tiempo real
- ✅ Administración de paradas

### Stack Tecnológico

| Componente | Versión |
|---|---|
| Python | 3.10+ |
| Django | 4.0+ |
| Django REST Framework | 3.14+ |
| PostgreSQL / SQLite | - |
| JWT | simplejwt |
| CORS | django-cors-headers |

---

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd rutas-universitarias-estudiantes/backend
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r backend/requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy backend/.env.example .env

# Editar .env con tus valores
```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Cargar datos iniciales (RBAC)

```bash
python manage.py seed_rbac
```

### 8. Ejecutar servidor

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

---

## 📁 Estructura del Proyecto

```
backend/
├── backend/                 # Configuración principal
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # Rutas principales
│   ├── wsgi.py
│   └── asgi.py
├── accounts/               # Autenticación y RBAC
│   ├── models.py           # Modelo de usuario extendido
│   ├── views.py            # Vistas de autenticación
│   ├── serializers.py
│   ├── permissions.py      # Permisos personalizados
│   ├── middleware.py
│   └── management/
│       └── commands/
│           └── seed_rbac.py
├── gps/                    # Monitoreo GPS
│   ├── models.py           # GPSPosicion, EventoDesvio
│   ├── views.py
│   └── serializers.py
├── rutas/                  # Gestión de rutas
│   ├── models.py           # Modelo de Ruta, Bus
│   ├── views.py
│   └── serializers.py
├── gestion_cupo/           # Control de cupos
│   ├── models.py           # Modelo de Cupo
│   ├── views.py
│   └── serializers.py
├── paradas/                # Administración de paradas
│   ├── models.py           # Modelo de Parada
│   ├── views.py
│   └── serializers.py
├── db.sqlite3              # Base de datos (desarrollo)
├── manage.py               # Script de gestión Django
└── requirements.txt        # Dependencias Python
```

---

## ⚙️ Configuración de Variables de Entorno

### Variables Críticas

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta (debe ser aleatoria en producción) | `django-insecure-...` |
| `DJANGO_DEBUG` | Modo debug (False en producción) | `True` / `False` |
| `DB_ENGINE` | Tipo de base de datos | `sqlite` / `postgres` |
| `EMAIL_HOST_PASSWORD` | Contraseña de email (App Password si es Gmail) | `wnbfflevmkkjnnlv` |

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

---

## 🔐 Autenticación

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

### Sesión (Cookie)

```bash
# Incluir cookies automáticamente
curl -c cookies.txt -b cookies.txt \
  -X POST http://localhost:8000/api/auth/login/ \
  -d "username=usuario&password=contraseña"
```

---

## 🧪 Testing

### Ejecutar pruebas

```bash
# Todas las pruebas
python manage.py test

# Pruebas de una app específica
python manage.py test accounts

# Con verbosidad
python manage.py test accounts -v 2

# Coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📊 Base de Datos

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate

# Revertir migración
python manage.py migrate app_name NÚMERO_ANTERIOR
```

### Seeders

```bash
# Cargar datos iniciales (RBAC)
python manage.py seed_rbac

# Crear superusuario
python manage.py createsuperuser
```

---

## 🛠️ Herramientas Útiles

### Admin Django

Accede a: `http://localhost:8000/admin`

- Usuarios: `http://localhost:8000/admin/accounts/user/`
- Rutas: `http://localhost:8000/admin/rutas/ruta/`
- Paradas: `http://localhost:8000/admin/paradas/parada/`

### Documentación API (Swagger)

Accede a: `http://localhost:8000/api/schema/swagger/`

### Shell Django

```bash
python manage.py shell
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

---

## 📦 Dependencias Principales

Ver archivo `requirements.txt`:

- Django 4.2+
- djangorestframework
- django-cors-headers
- djangorestframework-simplejwt
- drf-spectacular (API Schema)
- django-filter
- psycopg2-binary (PostgreSQL)

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

# 4. Usar PostgreSQL
DB_ENGINE=postgres

# 5. Ejecutar collectstatic
python manage.py collectstatic

# 6. Cambiar claves de email
EMAIL_HOST_PASSWORD=<contraseña-real>

# 7. Verificar CORS_ALLOWED_ORIGINS
```

---

## 📖 Documentación Adicional

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [JWT simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)

---

## 👥 Contribuidores

- Estudiantes de ING de Software B-2025

---

## 📄 Licencia

Este proyecto es propietario de la Universidad de La Guajira.

---

**Última actualización:** 11 de noviembre de 2025