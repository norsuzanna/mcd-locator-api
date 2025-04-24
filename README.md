# 🧠 McD Locator API – FastAPI + Supabase + OpenAI

This is the backend API for the **McD Locator** project – a geolocation-aware FastAPI service that powers outlet queries, chatbot interactions, and supports natural language searches for McDonald’s outlets in Malaysia.

---

## 📦 API Features

- 🔍 Query McDonald's outlets and features via REST API
- 💬 Chat endpoint for location-based and feature-specific searches (e.g. Wi-Fi, 24 hours)
- 📡 Supports geolocation queries like:
  - "McDonald's near KLCC"
  - "Outlets between Mid Valley and Pavilion"
- 🧠 OpenAI-powered chat logic (if `OPENAI_API_KEY` is configured)
- ⚡ Supabase PostgreSQL integration

---

## 🧱 Tech Stack

| Component   | Description                        |
|------------|------------------------------------|
| FastAPI     | Modern async web framework         |
| Supabase    | PostgreSQL backend + API client    |
| Uvicorn     | ASGI server for local dev/deploy   |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/norsuzanna/mcd-locator-api.git
cd mcd-locator-api
```

### 2. Create .env

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
OPENAI_API_KEY=sk-... (optional)
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the API Locally

```bash
uvicorn main:app --reload
```

## 📂 Project Structure

```bash
mcd-locator-api/
│
├── main.py              # FastAPI app and router
├── chat.py              # Chatbox logic + natural query handling
├── models.py            # Outlet data model (pydantic)
├── supabase.py          # Supabase client setup
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## 🔌 API Endpoints

| Method   | Endpoint  | Description  |
|----------|-----------|--------------|
| GET      | /scrape   | Web scraping |
| GET      | /outlets  | Outlet list  |
| POST     | /chat     | Chatbox      |

## 🧠 Sample Queries Supported
* "Which outlets open 24 hours?"

* "Show me outlets with EV charging"

* "Do any outlets offer birthday party?"

## 🛰 Deployment
This project supports deployment on Heroku or Railway.

Heroku Procfile Example:

```bash
web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
```

## 🙌 Acknowledgements
Built with ❤️ by [@norsuzanna](https://github.com/norsuzanna)<br>
Part of the McD Locator project: 🔗 Frontend: [norsuzanna/mcd-locator](https://github.com/norsuzanna/mcd-locator)

## 📄 License
This project is licensed under the MIT License.