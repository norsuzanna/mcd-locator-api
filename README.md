# 📦 McDonald's Malaysia Outlet Scraper & API

This project scrapes McDonald's Malaysia outlet data filtered by **Kuala Lumpur**, geocodes them, stores the data in a **Supabase PostgreSQL** database, and serves the data through a **FastAPI backend**.

---

## 🚀 Features

- ✅ Scrapes name, address, operating hours, and Waze link for each outlet
- ✅ Automatically geocodes address to get coordinates
- ✅ Stores results in Supabase PostgreSQL
- ✅ FastAPI-based REST API to serve the data
- ✅ Deployable to Heroku

---

## 🏗️ Tech Stack

| Layer        | Tech                                         |
| ------------ | -------------------------------------------- |
| Web Scraping | [Playwright](https://playwright.dev/python/) |
| Backend API  | [FastAPI](https://fastapi.tiangolo.com/)     |
| Database     | [Supabase PostgreSQL](https://supabase.com/) |
| Deployment   | [Heroku](https://www.heroku.com/)            |

---

## 📁 Project Structure

- **`db.py`**: Handles PostgreSQL database connections and queries.
- **`scraper.py`**: Contains the Playwright code to scrape McDonald's outlets and their details.
- **`main.py`**: The FastAPI application that serves as the backend API.
- **`models.py`**: Contains the Pydantic models used for validating API request and response data.
- **`Procfile`**: Used by Heroku to define the command to run the app.
- **`requirements.txt`**: Contains the Python dependencies.
- **`runtime.txt`**: Specifies the Python version to use for deployment in Heroku.
- **`.env`**: Stores sensitive information like API keys and database credentials (should be excluded from version control).

---

## 🧰 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mcd-scraper-api.git
cd mcd-scraper-api/backend
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 🛠️ Set Up Supabase PostgreSQL

Follow these steps to create and connect your database:

### 1. Create a Supabase Project

- Go to [https://supabase.com](https://supabase.com)
- Click **Start Project** and sign in
- Create a **new project**
- Set a name, password, and choose your region
- Wait for the project to be initialized

### 2. Get Database Credentials

- Go to the **Project Dashboard**
- Navigate to `Settings` → `Database`
- Copy the `Connection string` (use the `URI` format)

### 3. Create the Database Table

Go to the **SQL Editor** tab and run this SQL to create the `outlets` table:

```sql
CREATE TABLE outlets (
  id SERIAL PRIMARY KEY,
  name TEXT,
  address TEXT,
  operating_hours TEXT,
  waze_link TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION
);
```
