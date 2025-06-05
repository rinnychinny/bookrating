# 📚 Book Rating Recommender

A Django-based RESTful web application for rating books and receiving personalized recommendations. Built using the Goodreads-10k dataset for user-book rating data, tags, and metadata.

---

## 🚀 Project Features

- Input personal ratings for books
- Receive recommendations based on user similarity
- Browse and filter books by tag/genre
- Uses Django models and REST API endpoints
- Data sourced from the Goodreads-10k dataset

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rinnychinny/bookrating.git
cd bookrating
```

### 2. Set up a virtual environment

```bash
python -m venv venv
# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the Django project

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Then open your browser at [http://localhost:8000](http://localhost:8000)

---

## 📁 Dataset

This project uses the [Goodreads 10k dataset](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k), filtered to comply with project constraints (max 10,000 entries total). Only the top-rated users and their associated book ratings are included.

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`. Use `pip install -r requirements.txt` to replicate the environment.

---

## 🧠 License and Usage

This project is for educational and research purposes. The Goodreads-10k dataset is publicly shared for academic use under Kaggle’s data terms. Do not use this project or data for commercial applications.

---

## 👨‍💻 Author

**Rich P.** — Student Research Project

---
