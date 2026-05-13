# 🧱 3-Tier Portfolio Website

A clean 3-tier architecture portfolio built with **React**, **Node.js**, and **Python**.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  TIER 1 — Frontend                                  │
│  React (HTML/CSS/JS)  → index.html                  │
│  Fetches data from Backend API                      │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP REST
┌──────────────────────▼──────────────────────────────┐
│  TIER 2 — Backend                                   │
│  Node.js + Express  → backend/server.js             │
│  REST API on :5000                                  │
│  Routes: GET /api/projects, /api/skills             │
│          POST /api/contact                          │
└──────────────────────┬──────────────────────────────┘
                       │ Python subprocess
┌──────────────────────▼──────────────────────────────┐
│  TIER 3 — Database                                  │
│  Python + SQLite  → database/db_service.py          │
│  Tables: projects, skills, messages                 │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Initialize Database (Python)
```bash
cd database
python3 db_service.py
```

### 2. Start Backend (Node.js)
```bash
cd backend
npm install
npm start
# Running at http://localhost:5000
```

### 3. Open Frontend (React)
```bash
# Just open in a browser:
open frontend/index.html
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/health | Health check |
| GET | /api/projects | All projects from DB |
| GET | /api/skills | All skills from DB |
| POST | /api/contact | Save contact message |

---

## File Structure

```
portfolio/
├── frontend/
│   └── index.html          ← React app (CDN-based, no build needed)
├── backend/
│   ├── server.js           ← Express API server
│   └── package.json
├── database/
│   ├── db_service.py       ← Python SQLite service
│   └── portfolio.db        ← Auto-created on first run
└── README.md
```

---

> **Note:** The frontend works standalone with mock data if the backend isn't running. Full data flow requires all 3 tiers running.
