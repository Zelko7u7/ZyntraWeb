# ZyntraWeb

Aplicación web de fitness gamificada. Permite registrar entrenamientos, llevar un plan nutricional y ganar logros y XP conforme avanzas.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 6 + Django REST Framework |
| Autenticación | JWT (Simple JWT) |
| Base de datos | PostgreSQL |
| Frontend | Angular 19 |

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

## Configuración del Backend

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

Crea la base de datos en PostgreSQL y ejecuta las migraciones:

```bash
python manage.py migrate
python manage.py runserver
```

La API estará disponible en `http://localhost:8000`

## Configuración del Frontend

```bash
cd frontend
npm install
ng serve
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
