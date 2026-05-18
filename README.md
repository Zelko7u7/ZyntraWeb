# ZyntraWeb

Aplicación web de fitness gamificada. Permite registrar entrenamientos, llevar un plan nutricional y ganar logros y XP conforme avanzas.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 6 + Django REST Framework |
| Autenticación | JWT (Simple JWT) |
| Base de datos | PostgreSQL |
| Frontend | Angular 21 |

## Estructura del proyecto

```
ZyntraWeb/
├── Backend/     # API REST en Django
└── frontend/    # Aplicación Angular
```

## Funcionalidades

- Registro e inicio de sesión con JWT
- Gestión de rutinas y ejercicios
- Registro de entrenamientos por usuario
- Planes nutricionales y registro de comidas
- Sistema de progreso: XP, niveles y rangos
- Sistema de logros desbloqueables
- Chat con IA integrado

## Configuración rápida con Docker (recomendado)

Si tenés Docker Desktop instalado, levantar todo el stack es un solo comando:

```bash
docker compose up --build
```

Esto arranca:

- **Postgres 16** en el puerto `5432`
- **Backend Django** en `http://localhost:8000` (con migraciones y seed de niveles/rangos automáticos)
- **Frontend Angular** en `http://localhost:4200`

Para parar todo: `docker compose down`. Para borrar también la BD: `docker compose down -v`.

Variables de entorno opcionales (crear un `.env` en la raíz para sobreescribir defaults):

```env
DB_NAME=fitness_db
DB_USER=fitness_user
DB_PASSWORD=fitness_pass
SECRET_KEY=tu-secret-key
DEBUG=True
```

Si ya tenés Postgres corriendo en el puerto `5432` localmente, cambia el mapeo en `docker-compose.yml` (`"5433:5432"` por ejemplo) para evitar conflicto.

## Configuración manual (sin Docker)

### Backend

```bash
cd Backend
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Crea el archivo `.env` en la carpeta `Backend/` basándote en `.env.example`:

```env
DB_NAME=fitness_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

Crea la base de datos en PostgreSQL y ejecuta las migraciones y el seed:

```bash
python manage.py migrate
python manage.py init_data       # crea niveles, rangos y el logro "Iniciar cuenta"
python manage.py runserver
```

La API estará disponible en `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm start
```

La aplicación estará disponible en `http://localhost:4200`

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/token/` | Login, devuelve tokens JWT |
| POST | `/api/token/refresh/` | Renueva el access token |
| POST | `/api/users/register/` | Registro de usuario |
| GET/POST | `/api/workouts/rutinas/` | Rutinas de entrenamiento |
| GET/POST | `/api/workouts/entrenamientos/` | Historial de entrenamientos |
| GET/POST | `/api/nutrition/registrocomida/` | Registro de comidas |
| GET | `/api/progress/progreso/` | Progreso del usuario |
| GET | `/api/achievements/logrousuario/` | Logros desbloqueados |
| GET/POST | `/api/chat/chatconversacion/` | Conversaciones del chat |

## Autores

Proyecto universitario desarrollado por el equipo Zyntra.
