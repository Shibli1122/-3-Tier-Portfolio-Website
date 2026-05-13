# 🧱 3-Tier Portfolio Website
### A Beginner-Friendly Guide for Students

---

## 📚 What is a 3-Tier Architecture?

Before touching any code, let's understand the concept.

A **3-Tier Architecture** means your application is split into **3 separate layers**, each with its own job:

```
┌──────────────────────────────────────────────────────────────┐
│  TIER 1 — PRESENTATION (Frontend)                            │
│  What the USER SEES in their browser                         │
│  Technology: React (HTML + CSS + JavaScript)                 │
│  Runs on: Port 3000                                          │
└───────────────────────┬──────────────────────────────────────┘
                        │
                   HTTP Requests
                  (asks for data)
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  TIER 2 — LOGIC (Backend)                                    │
│  The BRAIN — handles rules, processes requests               │
│  Technology: Node.js + Express                               │
│  Runs on: Port 5000                                          │
└───────────────────────┬──────────────────────────────────────┘
                        │
                   Python calls
                 (reads/writes data)
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  TIER 3 — DATA (Database)                                    │
│  Where all DATA is STORED permanently                        │
│  Technology: Python + PostgreSQL                             │
│  Runs on: Port 5432                                          │
└──────────────────────────────────────────────────────────────┘
```

### 🤔 Why split into 3 tiers?

| Reason | Explanation |
|--------|-------------|
| **Separation of concerns** | Each layer does ONE job and does it well |
| **Security** | Database is never directly exposed to the user |
| **Scalability** | You can upgrade each layer independently |
| **Team work** | Frontend devs, backend devs, and DBAs can work separately |

---

## 🗄️ Why PostgreSQL? (Not SQLite)

You might have used **SQLite** before — it stores data in a single file. It's fine for learning, but not for real apps.

**PostgreSQL** is a professional-grade database used by companies like Instagram, Spotify, and Reddit.

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Type | File-based | Full server |
| Multiple users | ❌ No | ✅ Yes |
| Production-ready | ❌ No | ✅ Yes |
| Handles big data | ❌ Limited | ✅ Yes |
| Used in industry | Rarely | Very common |

---

## 🗂️ Project File Structure

```
3-Tier-Portfolio-Website/
│
├── frontend/
│   └── index.html          ← The React UI (what users see)
│
├── backend/
│   ├── server.js           ← Node.js API server (the brain)
│   └── package.json        ← Node.js dependencies list
│
├── database/
│   └── db_service.py       ← Python script that talks to PostgreSQL
│
└── README.md               ← This file!
```

---

## 🚀 Full Setup Guide (EC2 Ubuntu)

Follow these steps **in order**. Don't skip any!

---

### STEP 1 — Update Your System

Always start by updating Ubuntu's package list:

```bash
sudo apt update
sudo apt upgrade -y
```

---

### STEP 2 — Install Node.js

Node.js runs our backend server:

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node -v     # should show v18.x.x
npm -v      # should show a version number
```

---

### STEP 3 — Install Python & pip

Python runs our database service:

```bash
sudo apt install -y python3 python3-pip

# Verify
python3 --version   # should show Python 3.x.x
```

---

### STEP 4 — Install PostgreSQL

This installs the PostgreSQL database server:

```bash
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL and enable it on boot
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify it's running
sudo systemctl status postgresql
# You should see: Active: active (running)
```

---

### STEP 5 — Set Up the PostgreSQL Database

Now we create a database and a user for our app.

```bash
# Switch to the postgres admin user
sudo -i -u postgres

# Open the PostgreSQL command line
psql
```

Inside `psql`, run these commands **one by one**:

```sql
-- Create a new database user
CREATE USER portfolio_user WITH PASSWORD 'portfolio_pass';

-- Create the database
CREATE DATABASE portfolio_db;

-- Give our user full access to the database
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;

-- Exit psql
\q
```

Then exit back to ubuntu user:
```bash
exit
```

---

### STEP 6 — Install Python PostgreSQL Library

Python needs a library called `psycopg2` to talk to PostgreSQL:

```bash
pip3 install psycopg2-binary
```

---

### STEP 7 — Set Up Project Folders

Organize your files into the right folders:

```bash
# Go into the project
cd ~/Student-test/3-Tier-Portfolio-Website

# Create folders
mkdir -p frontend backend database

# Move files
cp backend_server.js backend/server.js
cp backend_package.json backend/package.json
cp database_service.py database/db_service.py
cp portfolio_frontend.html frontend/index.html
```

---

### STEP 8 — Initialize the Database

This creates all the tables and fills them with sample data:

```bash
cd database
python3 db_service.py
cd ..
```

✅ You should see: `PostgreSQL database initialized successfully.`

---

### STEP 9 — Start the Backend

```bash
cd backend
npm install
node server.js &
cd ..
```

✅ You should see: `🚀 Backend running on http://localhost:5000`

Test it works:
```bash
curl http://localhost:5000/api/health
# Should return: {"status":"ok","tier":"backend",...}
```

---

### STEP 10 — Serve the Frontend

```bash
sudo npm install -g http-server

cd frontend
http-server -p 3000 &
```

✅ Frontend is now running on port 3000.

---

### STEP 11 — Open AWS Security Group Ports

Your EC2 has a firewall. You need to open ports so the internet can reach your app.

1. Go to **AWS Console → EC2 → Instances**
2. Click your instance → **Security** tab → click the Security Group link
3. Click **Edit inbound rules** → **Add rule**:
   - Type: `Custom TCP` | Port: `3000` | Source: `0.0.0.0/0` → (Frontend)
   - Type: `Custom TCP` | Port: `5000` | Source: `0.0.0.0/0` → (Backend API)
4. Click **Save rules**

---

### STEP 12 — Open in Browser

Find your EC2 Public IP in the AWS Console, then visit:

```
http://<your-ec2-public-ip>:3000
```

🎉 Your 3-tier portfolio is live!

---

## 🔄 How Data Flows (Step by Step)

Here's exactly what happens when someone visits your portfolio:

```
1. User opens browser → http://your-ip:3000

2. React (frontend) loads and sends a request:
   GET http://your-ip:5000/api/projects

3. Node.js (backend) receives the request and runs:
   python3 db_service.py → calls get_all_projects()

4. Python connects to PostgreSQL and runs:
   SELECT * FROM projects ORDER BY created_at DESC

5. PostgreSQL returns the data to Python
   Python returns it to Node.js
   Node.js sends it back to React as JSON

6. React displays the projects as cards on the screen ✅
```

---

## 🛠️ Useful Commands

```bash
# Check if backend is running
ps aux | grep node

# Check if PostgreSQL is running
sudo systemctl status postgresql

# View data directly in PostgreSQL
sudo -i -u postgres
psql -d portfolio_db
SELECT * FROM projects;
\q

# Stop everything
pkill -f "node server.js"
pkill -f "http-server"

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## ❌ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `connection refused` on port 5432 | PostgreSQL not running | `sudo systemctl start postgresql` |
| `psycopg2 not found` | Library not installed | `pip3 install psycopg2-binary` |
| `role "portfolio_user" does not exist` | DB user not created | Redo Step 5 |
| `cannot connect to backend` in browser | Port 5000 not open | Check AWS Security Group (Step 11) |
| `EADDRINUSE: port 5000` | Backend already running | `pkill -f "node server.js"` then restart |

---

## 📝 Summary — What Each File Does

| File | Technology | Job |
|------|-----------|-----|
| `frontend/index.html` | React | Shows the UI to the user |
| `backend/server.js` | Node.js + Express | Handles API requests |
| `database/db_service.py` | Python + psycopg2 | Talks to PostgreSQL |
| `backend/package.json` | npm | Lists Node.js libraries needed |

---

*Built for learning 3-Tier Architecture with React · Node.js · Python · PostgreSQL*
