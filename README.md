# Todo App con IA 

Esta carpeta aloja la version del proyecto del curso "LLM e IA" del instructor Julio Colomer. Es un ejemplo concreto que integra una interfaz de tareas simples con llamadas a APIs, un backend FastAPI con Postgres y una cadena de LangChain para pedir a GPT-4o-mini que escriba poemas cortos. La base inicial fue el repositorio https://github.com/AI-LLM-Bootcamp/1024-langchain-plus-todo-app y aqui se aplicaron mejoras propias en el frontend, el modelado y los flujos de API.

## Tecnologias claves
- Frontend Next.js 16 + React 19, turbopack en dev, CSS modulado y layout sobrio.
- Backend FastAPI con routers y SQLAlchemy; la configuracion usa `DATABASE_URL` apuntando a Postgres y `OPENAI_API_KEY` para LangChain.
- Modelado: `models.py` define la tabla `todos`, `alembic` contiene las migraciones y los CRUD se separan en `crud.py`.
- IA: LangChain con `ChatOpenAI` (modelo `gpt-4o-mini`), prompt `write_poem_prompt` y `StrOutputParser` enganchados desde `/todos/write-poem/{id}`.

## Arquitectura
### Backend (todoapp-LC-backend)
1. Crear entorno, instalar dependencias (`pip install -r requirements.txt` o `poetry install`).
2. Definir variables: `DATABASE_URL=postgres://user:pass@host:5432/dbname`, `OPENAI_API_KEY=...`.
3. Ejecutar migraciones `alembic upgrade head`.
4. Levantar con `uvicorn main:app --reload --host 0.0.0.0 --port 8000`.

### Frontend (todoapp-LC-frontend)
1. `npm install`.
2. Crear `.env` con `NEXT_PUBLIC_API_URL=http://localhost:8000` y apuntar al backend.
3. Ejecutar `npm run dev` para turbopack o `npm run build` y `npm run start` para produccion.

### Postgres y modelado
- El backend se conecta via SQLAlchemy a una base Postgres; la aplicacion define un CRUD basico sobre `ToDo`.
- El ejemplo es util cuando se quiere mostrar versioning de esquemas, uso de migraciones y ensenanza de consultas simples en un contexto de LLM.

## IA, prompts y casos de uso
- El prompt `Escribe un poema corto en espanol con el siguiente texto: {text}` usa LangChain para demostrar como un LLM puede complementar tareas administrativas con generacion creativa.
- Casos de uso profesionales: 1) dashboards internos que combinan datos operativos con resenas o mensajes generados por IA; 2) generacion automatica de contenido o resueltas para equipos de soporte; 3) prototipos de asistentes que recomiendan acciones mientras se trabaja en listados de tareas.
- Tambien se expone `/todos/write-poem/{id}` para invocar el modelo desde cualquier cliente y `/todos` maneja el resto del CRUD.

## Documentacion y sitios disponibles
- Dashboard FastAPI en `http://localhost:8000/docs` y `http://localhost:8000/redoc`.
- Frontend en `http://localhost:3000`.
- LangChain se configura en `routers/todos.py` y se puede extender con nuevos prompts o modelos.

## Recursos y referencias
- Repositorio base del instructor: https://github.com/AI-LLM-Bootcamp/1024-langchain-plus-todo-app
- Mejores propias en frontend, modelado y API.
- Documentacion oficial FastAPI, LangChain y Next.js cuando se requiera extendion.

## Capturas
- Swagger/API FastAPI (ejemplo en `/docs`):  
  ![API 1](docs/screenshots/api-1.jpg)
- Script de llamadas y consola abierta en FastAPI:  
  ![API 2](docs/screenshots/api-2.jpg)
- Interfaz principal del frontend de tareas:  
  ![Inicio](docs/screenshots/inicio.jpg)
- Popup de poema generado con IA:  
  ![Poema IA](docs/screenshots/poema-ia.jpg)
