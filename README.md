# Holiday Shift System

A full-stack web application for managing holiday shifts, featuring a public read-only view for collaborators and a secure administrative dashboard for management.

The system is built with a modern frontend architecture (Vue 3 + Vite) and a robust Python backend (FastAPI), utilizing **Databricks** as the persistence layer.

## 🚀 Technology Stack

### Frontend
- **Framework**: [Vue 3](https://vuejs.org/) (Composition API)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **State Management**: [Pinia](https://pinia.vuejs.org/)
- **Routing**: [Vue Router](https://router.vuejs.org/)
- **HTTP Client**: Axios (with Interceptors for Auth)
- **UI/UX**: Custom CSS (Glassmorphism aesthetics), Lucide Icons
- **Language**: JavaScript (ES6+)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: Databricks SQL (via `databricks-sql-connector`)
- **Authentication**: HTTP Basic Auth (Custom Implementation)
- **Runtime**: Python 3.10+

## 🏛️ Architecture & Features

### Public Access (`/`)
- Read-only view accessible to all users without login.
- Real-time search by Holiday Name, Collaborator Name, or Registration Number (Matrícula).
- Responsive grid layout displaying shift cards.

### Administrative Dashboard (`/admin`)
- Protected by Authentication Guard.
- Full CRUD operations:
    - **Create**: Add new shifts with validation (Name, Collaborator, Matricula, Date).
    - **Read**: View all shifts.
    - **Delete**: Remove shifts.
- Session management via Pinia Store and LocalStorage.

### Database Schema (`holiday_shifts_v4`)
- Hosted on Databricks (Catalog: `main`, Schema: `default`).
- Columns: `id` (UUID), `name`, `collaborator_name`, `registration_number`, `holiday_date`, `created_at`.

## 🤖 AI-Oriented Programming

This project serves as a case study in **AI-Oriented Programming**. It was constructed through a high-bandwidth collaborative workflow between a human developer and an Agentic AI (Antigravity).

### Key Characteristics of the Workflow

1.  **Intent-Driven Development**:
    - Instead of writing boilerplate, the developer expressed high-level intents (e.g., "Rebuild the frontend with Vue 3", "Add collaborator fields").
    - The AI agent translated these intents into technical implementation plans, bridging the gap between business requirements and code.

2.  **Agentic Context Awareness**:
    - The AI maintained a continuous context of the project state (`task.md`, `implementation_plan.md`).
    - It autonomously analyzed the existing backend logic to ensure exact compatibility with the new frontend (e.g., matching Pydantic models with Vue forms).

3.  **Self-Correction & Verification**:
    - The workflow included automated and manual verification steps.
    - When issues arose (e.g., a blank screen due to a syntax error in `router/index.js`), the AI utilized terminal outputs and file reads to diagnose and patch the bug autonomously, demonstrating resilience.

4.  **Rapid Prototyping & Refinement**:
    - The project evolved from a standard dashboard to a dual-view system (Public/Admin) in minutes.
    - Localization (PT-BR) and UI polishing (premium glassmorphism) were applied as iterative layers on top of the functional core.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- Databricks Connection Details (Server Hostname, HTTP Path, Token)

### 1. Backend Setup
Navigate to the root directory and configure environment variables in `.env` (already configured in this environment).

```powershell
pip install -r requirements.txt
python backend/main.py
```
*Server will start on `http://127.0.0.1:8080`*

### 2. Frontend Setup
Navigate to the frontend directory:

```powershell
cd frontend
npm install
npm run dev
```
*Application will be served at `http://localhost:5173`*

## 📝 License
Proprietary - Internal Use Only.
