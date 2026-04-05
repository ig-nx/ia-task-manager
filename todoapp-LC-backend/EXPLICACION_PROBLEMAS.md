# Explicación de lo que pasó y cómo se arregla

Este proyecto es una API de tareas con FastAPI, SQLAlchemy, Alembic y una base de datos PostgreSQL en Neon.

## Estructura básica del código

- `main.py`: crea la app FastAPI y monta los routers.
- `routers/todos.py`: define los endpoints `/todos`.
- `crud.py`: hace las consultas a la base de datos.
- `models.py`: define la tabla `todos` en SQLAlchemy.
- `schemas.py`: valida lo que entra y sale por la API.
- `database.py`: crea la conexión a la base usando `DATABASE_URL`.
- `alembic/env.py`: usa la conexión para correr migraciones.
- `alembic/versions/...`: contiene la migración que crea la tabla `todos`.

## Qué error estaba pasando

Había varios problemas mezclados:

### 1. Alembic estaba usando variables viejas

`alembic/env.py` buscaba estas variables:

- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_NAME`

Pero tu archivo `.env` ya usa una sola variable:

- `DATABASE_URL`

Por eso aparecía:

```text
KeyError: 'DATABASE_USER'
```

## 2. La URL de conexión estaba mal escrita

Primero la URL tenía una forma incorrecta, por ejemplo algo parecido a:

```env
DATABASE_URL=postgresql:psycopg2://...
```

Eso no es válido. SQLAlchemy espera este formato:

```env
DATABASE_URL=postgresql+psycopg2://usuario:password@host:puerto/base_de_datos?sslmode=require&channel_binding=require
```

La parte importante es esta:

- `postgresql+psycopg2://`

Si esa parte está mal, Alembic no puede ni interpretar la conexión.

## 3. La tabla `todos` no existía

Aunque la app levantaba, al hacer `GET /todos` salía:

```text
relation "todos" does not exist
```

Eso significa:

- la base de datos sí existe
- pero la tabla `todos` no estaba creada todavía

La tabla se crea con la migración:

```text
alembic/versions/8fb8217edc35_create_todos_table.py
```

## Cómo se arregla correctamente

### Paso 1: dejar bien el `.env`

Debe tener una URL completa en una sola línea.

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg2://neondb_owner:TU_PASSWORD@TU_HOST/neondb?sslmode=require&channel_binding=require
```

### Paso 2: correr migraciones

Desde la carpeta del backend:

```bash
alembic upgrade head
```

Eso crea la tabla `todos` en la base real.

### Paso 3: levantar el backend

```bash
uvicorn main:app --reload
```

### Paso 4: probar la API

Si la base está vacía, `GET /todos` debería responder:

```json
[]
```

## Qué hace cada archivo en este problema

### `database.py`

Lee `DATABASE_URL` y crea el engine de SQLAlchemy.

### `alembic/env.py`

Le dice a Alembic qué base usar para ejecutar migraciones.

### `models.py`

Define cómo es la tabla `todos`.

### `crud.py`

Hace consultas como:

- listar tareas
- crear tarea
- borrar tarea
- actualizar tarea

### `routers/todos.py`

Expone las rutas:

- `GET /todos`
- `POST /todos`
- `GET /todos/{id}`
- `PUT /todos/{id}`
- `DELETE /todos/{id}`

## Otro error que apareció

En `POST /todos` salió un `422 Unprocessable Content`.

Eso pasó porque el JSON enviado tenía un valor inválido en `completed`.

`completed` debe ser booleano:

```json
{
  "name": "Estudiar",
  "completed": true
}
```

No debe ser texto como:

```json
{
  "name": "Estudiar",
  "completed": "tru2222e"
}
```

## Resumen corto

- El backend usa PostgreSQL en Neon.
- `DATABASE_URL` debe estar bien escrita.
- Alembic necesita esa URL para crear la tabla.
- Si no se corre `alembic upgrade head`, `todos` no existe.
- Si `completed` no es booleano, `POST /todos` devuelve 422.

## Flujo correcto desde cero

1. Crear la base de datos.
2. Poner `DATABASE_URL` en `.env`.
3. Ejecutar `alembic upgrade head`.
4. Levantar `uvicorn main:app --reload`.
5. Probar `GET /todos`.
6. Crear un todo con `POST /todos`.

