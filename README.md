# TechLearn LMS

This repository contains a multi-container LMS application:
- lms_database: MongoDB database
- lms_backend: FastAPI backend API (port 3001)
- lms_frontend: React frontend (port 3000)

This step implements baseline backend, database integration, and minimal frontend to list courses.

## Backend (FastAPI)

### Features
- Environment-based configuration (.env) with required secrets (no hardcoded secrets)
- MongoDB (Motor) async client with startup/shutdown lifecycle
- Health endpoint: GET /health
- Courses endpoints:
  - GET /api/v1/courses?category=...&published=... (list with filters)
  - POST /api/v1/courses (create) [placeholder auth allows all]
  - GET /api/v1/courses/{id}
- Centralized error handling and standard response envelope
- CORS configured via CORS_ORIGINS
- OpenAPI docs at /docs

### Environment Variables
Copy lms_backend/.env.example to .env and set values:
- APP_ENV (default development)
- PORT (default 3001)
- MONGO_URI (required)
- MONGO_DB_NAME (required)
- JWT_SECRET (required placeholder)
- JWT_ALGORITHM (default HS256)
- CORS_ORIGINS (csv; default http://localhost:3000)

### Run Backend
From lms_backend:
1. python -m pip install -r requirements.txt
2. Create .env
3. python -m src.api.main
   - Binds to 0.0.0.0:PORT (default 3001)

## Frontend (React)
- Minimal shell with pages:
  - Home
  - Courses List (fetches /api/v1/courses)
  - Course Details (fetches /api/v1/courses/:id)
- Uses REACT_APP_API_BASE_URL (default http://localhost:3001)

## Database (MongoDB)
- Used by backend via MONGO_URI and MONGO_DB_NAME
- No scripts provided here; run a MongoDB instance accessible to backend.

## Notes / TODO
- Implement real authentication and role-based authorization
- Add pagination, sorting, and validation improvements
- Expand domain models (modules, lessons, enrollments)
- Add tests and CI
