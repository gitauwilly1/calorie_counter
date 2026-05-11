# Calorie Counter

## Contributors
[William Gitau]

---

## Your Path to Nutritional Awareness

Calorie Counter is a comprehensive Django web application designed to bridge the gap between daily eating habits and nutritional awareness. It empowers users through a clear data-driven journey: **Log → Track → Analyze**.

---

## Problem Statement

A significant percentage of individuals fail to maintain healthy eating habits due to:
- Inability to accurately track daily caloric intake
- Lack of visibility into nutritional patterns over time
- Overly complex tracking interfaces that discourage consistent logging
- Absence of historical data to identify trends

---

## Solution Overview

Calorie Counter provides a structured nutritional tracking journey:

| Phase | Description |
|-------|-------------|
| **Log** | Rapid entry of food items with caloric values and instant database persistence |
| **Track** | Real-time dashboard calculating total daily consumption with progress indicators |
| **Analyze** | Historical date filtering and weekly summaries to identify nutritional patterns |

---

## Design System

**Primary Colors:**
- Blue (Focus, Trust, Clarity)
- Gray (Cleanliness, Professionalism)

**Typography:**
- Headers: System Sans-Serif
- Body: System Sans-Serif

**Layout:** Utility-first, card-based responsive grid built with Tailwind CSS.

---

## Key Features

- **Daily Calorie Tracking** - Log food items with calories for any date.
- **Dynamic CRUD Operations** - Add and remove food entries with immediate UI feedback.
- **Progress Visualization** - Interactive progress bar comparing intake against 2,000 calorie goal.
- **Date Navigation** - Browse and manage food entries across different dates.
- **Weekly Summaries** - At-a-glance view of daily calorie totals for the current week.
- **Admin Dashboard** - Comprehensive admin panel with custom actions and calorie level indicators.
- **Responsive Design** - Mobile-first layout optimized for tracking on any device.
- **PostgreSQL Database** - Robust relational database for reliable data persistence.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 6** | Backend framework & ORM |
| **PostgreSQL** | Relational database management |
| **Tailwind CSS** | Modern utility-first styling |
| **Render** | Cloud deployment & hosting |

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Local Development

1. **Clone the Repository:**
    ```
    git clone https://github.com/gitauwilly1/calorie_counter.git
    cd calorie_counter
    ```

2. **Create Virtual Environment:**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: source venv/Scripts/activate
    ```

3. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Set Up PostgreSQL Database:**
    ```
    CREATE DATABASE calorie_tracker_db;
    CREATE USER calorie_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE calorie_tracker_db TO calorie_user;
    ```

5. **Configure Environment Variables:**
    Create a `.env` file in the project root:
    ```
    DJANGO_SECRET_KEY=your-secret-key
    DEBUG=True
    DB_NAME=calorie_tracker_db
    DB_USER=calorie_user
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

6. **Run Migrations:**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Create Admin User:**
    ```
    python manage.py createsuperuser
    ```

8. **Start Development Server:**
    ```
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000/` in your browser.

---

## Live Demo

Experience the application live at: **[Calorie Counter on Render](https://calorie-counter.onrender.com)**

---

## Known Bugs

There are no known bugs at this time.

---

## License

* **License:** MIT License.

---

## Support and Information

**Email:** [gitauwilly254@gmail.com]
**GitHub:** [https://github.com/gitauwilly1/calorie_counter](https://github.com/gitauwilly1/calorie_counter)