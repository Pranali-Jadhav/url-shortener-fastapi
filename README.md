# 🚀 URL Shortener (FastAPI + PostgreSQL)

A production-style URL shortening service built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.
The project demonstrates strong backend fundamentals including API design, validation, rate limiting, link expiry, database integration, and clean modular architecture.

---

## ✨ Features

* 🔗 Shorten any long URL
* 🚀 Fast redirection using short codes
* ✔ URL validation using Pydantic
* 📊 Click tracking for each link
* ⏳ Configurable link expiry (minutes-based TTL)
* 🔐 Per-IP rate limiting to avoid abuse
* 🎲 Random Base62 short code generation
* 🗄 Persistent storage using PostgreSQL
* 🧩 Modular structure with routers, schemas, models, utils
* 📘 Interactive API docs using Swagger UI (`/docs`)

---

## 🏗 Project Structure

```
url_shortener/
│── main.py               # FastAPI app entry point
│── database.py           # DB engine + session management
│── models.py             # SQLAlchemy models
│── schemas.py            # Pydantic schemas
│── utils.py              # Helper functions (short code generator)
│── routers/
│     └── url.py          # All URL shortener APIs
│── requirements.txt
│── README.md
```

---

## 🛠 Tech Stack

* **Python 3**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Pydantic**
* **Uvicorn**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <your_repo_url>
cd url_shortener
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure PostgreSQL

Create a database:

```sql
CREATE DATABASE shortener_db;
```

Update your database URL in `database.py`:

```
postgresql://<username>:<password>@localhost:5432/shortener_db
```

### 5️⃣ Start the application

```bash
uvicorn main:app --reload
```

Open the API docs:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### ➤ POST `/shorten`

Create a new shortened URL.

**Request Body:**

```json
{
  "original_url": "https://example.com",
  "expires_in_minutes": 10
}
```

**Response:**

```json
{
  "short_url": "http://127.0.0.1:8000/Ab12XyZ"
}
```

---

### ➤ GET `/{short_code}`

Redirect to the original URL.
Automatically increases the click count.

---

## 🔒 Rate Limiting

To prevent abuse, the system limits:

> **Max 5 URL creations per IP per minute**

If exceeded, returns:

```
429 Too Many Requests
```

---

## ⏳ Link Expiry

Users can optionally provide:

```
expires_in_minutes
```

Example:
If set to `10`, the link will expire 10 minutes from creation.

If expired, redirect returns:

```
410 Gone – Short URL has expired
```

---

