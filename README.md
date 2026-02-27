# 🚀 Project Task Management API

A full-stack backend API built with **FastAPI** for managing freelance projects, tasks, and payments between **buyers** and **developers**.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Roles & Permissions](#roles--permissions)
- [Deployment](#deployment)

---

## Overview

This platform connects **buyers** (who create projects and tasks) with **developers** (who complete tasks and submit solutions). It features JWT-based authentication, role-based access control, file uploads, hourly-rate payments, and an admin dashboard.

### Key Features

- 🔐 **JWT Authentication** — Secure login & registration with role-based access
- 👥 **Multi-Role System** — Buyer, Developer, and Admin roles
- 📁 **Project Management** — Buyers create and manage projects
- ✅ **Task Lifecycle** — Create → Start → Submit → Pay workflow
- 💰 **Payment Processing** — Automatic cost calculation (hourly rate × hours spent)
- 📤 **File Uploads** — Developers submit solution files with tasks
- 📊 **Admin Dashboard** — Platform-wide statistics and analytics

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework |
| **SQLAlchemy** | ORM / Database toolkit |
| **PostgreSQL** | Database |
| **python-jose** | JWT token handling |
| **Passlib** | Password hashing (PBKDF2-SHA256) |
| **Uvicorn** | ASGI server |
| **Pydantic** | Data validation & serialization |

---

## Architecture

```
app/
├── core/
│   ├── config.py          # App settings (env variables)
│   ├── database.py        # SQLAlchemy engine & session
│   └── security.py        # Password hashing & JWT utils
├── dependencies/
│   └── role_checker.py    # Auth & role-based access control
├── models/
│   ├── user.py            # User model
│   ├── project.py         # Project model
│   ├── task.py            # Task model
│   └── payment.py         # Payment model
├── routes/
│   ├── auth.py            # Auth endpoints
│   ├── project.py         # Project endpoints
│   ├── task.py            # Task endpoints
│   ├── payment.py         # Payment endpoints
│   └── admin.py           # Admin endpoints
├── schemas/
│   ├── user.py            # User request/response schemas
│   ├── project.py         # Project schemas
│   ├── task.py            # Task schemas
│   └── payment.py         # Payment schemas
└── main.py                # FastAPI app entry point
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

📖 **Interactive API Docs**: `http://localhost:8000/docs`

---

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/your_database
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## API Endpoints

### 🔐 Auth (`/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/auth/register` | Register a new user | ❌ |
| `POST` | `/auth/login` | Login & get JWT token | ❌ |
| `GET` | `/auth/me` | Get current user profile | ✅ |
| `GET` | `/auth/userlist` | List users (filter by role) | ❌ |

**Register** — Request Body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "buyer"  // "buyer", "developer", or "admin"
}
```

**Login** — Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "role": "buyer"
}
```

---

### 📁 Projects (`/projects`)

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `POST` | `/projects/` | Create a new project | ✅ | Buyer |
| `GET` | `/projects/mine` | Get my projects | ✅ | Buyer / Developer |

> **Note**: Developers see projects where they have assigned tasks. Buyers see projects they created.

---

### ✅ Tasks (`/tasks`)

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `POST` | `/tasks/` | Create a task for a project | ✅ | Buyer |
| `GET` | `/tasks/mine` | Get my tasks | ✅ | Buyer / Developer |
| `GET` | `/tasks/project/{project_id}` | Get all tasks in a project | ✅ | Any |
| `GET` | `/tasks/{task_id}` | Get a specific task | ✅ | Any |
| `POST` | `/tasks/{task_id}/start` | Start working on a task | ✅ | Developer |
| `POST` | `/tasks/{task_id}/submit` | Submit completed task | ✅ | Developer |

**Create Task** — Request Body:
```json
{
  "title": "Design Landing Page",
  "description": "Create a responsive landing page",
  "project_id": "uuid",
  "assigned_developer": "uuid",
  "hourly_rate": 50.0
}
```

**Submit Task** — `multipart/form-data`:
- `hours_spent` (float) — Hours worked
- `file` (file) — Solution file upload

**Task Status Flow**:
```
todo → in_progress → submitted → paid
```

---

### 💰 Payments (`/payments`)

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `POST` | `/payments/{task_id}` | Pay for a submitted task | ✅ | Buyer |

> Payment amount is automatically calculated: `hourly_rate × hours_spent`

---

### 📊 Admin (`/admin`)

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/admin/stats` | Get platform statistics | ✅ | Admin |

**Response**:
```json
{
  "total_users": 15,
  "total_projects": 8,
  "total_tasks": 25,
  "tasks_by_status": {
    "todo": 5,
    "in_progress": 8,
    "submitted": 7,
    "paid": 5
  },
  "total_revenue": 12500.00,
  "total_paid_hours": 250.0
}
```

---

## Database Schema

```mermaid
erDiagram
    USERS {
        uuid id PK
        string name
        string email UK
        string password_hash
        string role
    }

    PROJECTS {
        uuid id PK
        string title
        string description
        uuid buyer_id FK
    }

    TASKS {
        uuid id PK
        string title
        string description
        uuid project_id FK
        uuid assigned_developer FK
        float hourly_rate
        string status
        float hours_spent
        string solution_file
    }

    PAYMENTS {
        uuid id PK
        uuid task_id FK
        uuid buyer_id FK
        float amount
        string status
    }

    USERS ||--o{ PROJECTS : "creates (buyer)"
    USERS ||--o{ TASKS : "assigned to (developer)"
    PROJECTS ||--o{ TASKS : "contains"
    TASKS ||--o| PAYMENTS : "paid via"
    USERS ||--o{ PAYMENTS : "pays (buyer)"
```

---

## Roles & Permissions

| Feature | Buyer | Developer | Admin |
|---------|:-----:|:---------:|:-----:|
| Create projects | ✅ | ❌ | ❌ |
| Create tasks | ✅ | ❌ | ❌ |
| View own projects/tasks | ✅ | ✅ | ❌ |
| Start a task | ❌ | ✅ | ❌ |
| Submit a task | ❌ | ✅ | ❌ |
| Pay for a task | ✅ | ❌ | ❌ |
| View platform stats | ❌ | ❌ | ✅ |

---

## Deployment

This project is deployed on **[Render](https://render.com)**.

**Live URL**: `https://project-task-backend-fmq6.onrender.com`

### Deploy to Render

1. Push your code to GitHub
2. Create a new **Web Service** on Render
3. Connect your repository
4. Set the **Build Command**: `pip install -r requirements.txt`
5. Set the **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add your environment variables in the Render dashboard

> ⚠️ **Note**: Render's free tier uses an ephemeral filesystem. Uploaded files will not persist across deploys. For production, consider using cloud storage (e.g., AWS S3, Cloudinary).

---

## License

This project is built as a full-stack interview task.
