# 📚 Book Rating Recommender

A Django-based RESTful web application for rating books and receiving personalized recommendations. Built using the Goodreads-10k dataset for user-book rating data, tags, and metadata.

---

## 🚀 Project Features

- Input and view personal ratings for books
- Receive recommendations based on user similarity (also-loved)
- Browse and filter books by author
- Uses Django models and REST API endpoints
- Data sourced from the Goodreads-10k dataset
- Bulk loader command provided (bulk_load)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/rinnychinny/bookrating.git
cd bookrating

### 2. Set up a virtual environment

python -m venv venv

# Activate the virtual environment

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up the Django project

cd bookrating_project
python manage.py makemigrations
python manage.py migrate

### 5. Load filtered data into the database (<10k csv lines)

(from bookrating_project)
python scripts/loader.py

### 6. Run the development server

python manage.py runserver

Then open your browser at [http://localhost:8000](http://localhost:8000)

---

## 📁 Dataset

This project uses the [Goodreads 10k dataset](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k), filtered to comply with project constraints (max 10,000 entries total). Only some users and their associated book ratings are included.

The filtered datasets are in \goodbooks-10k-filtered\ (filtered_books.csv and filtered_ratings.csv), along with the .ipynb notebook used to produce the filtered data.

---

## 📁 Bulk load

Custom Django command bulk_load provided with 2 optional named arguments. Usage:

python manage.py bulk_load --books 'fname_books.csv' --ratings 'fname_ratings.csv'

## 📦 Requirements

All dependencies are listed in `requirements.txt`. Use `pip install -r requirements.txt` to replicate the environment.

---

## 🧠 License and Usage

This project is for educational and research purposes. The Goodreads-10k dataset is publicly shared for academic use under Kaggle’s data terms. Do not use this project or data for commercial applications.

---

## 👨‍💻 Author

**Rich P.** — Student Research Project

---
