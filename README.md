# 🐾 Animal Shelter Management System

A full-stack Django web application for managing animal shelters. Add animals, track adopters, upload photos, and search through records — all protected behind a secure login system.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## 📋 Features

### 🔐 Authentication
- User login/logout system
- Protected routes (no access without login)

### 🐶 Animal Management (CRUD)
- **Add** new animals with name, breed, age, and photo
- **Edit** animal details
- **Delete** animals from the system
- **Upload photos** stored in media folder

### 👤 Adopter Management (CRUD)
- **Add** adopter profiles
- **Edit** adopter information
- **Delete** adopter records

### 🔍 Search
- Search bar to quickly find animals or adopters

### 🎨 Frontend
- Clean, custom CSS styling
- Django templates for dynamic pages

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django** | Backend framework |
| **SQLite** | Database |
| **HTML5** | Structure |
| **CSS3** | Styling |
| **Django Templates** | Dynamic rendering |

---

## 🚀 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/loujayntoumi0-sudo/animal-shelter.git
   cd animal-shelter

2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4.Set up environment variable
# Create .env file and add your secret key
echo "DJANGO_SECRET_KEY=your-secret-key-here" > .env

5.Run migrations
python manage.py migrate

6.Create superuser (admin access)
python manage.py createsuperuser

7. Launch the server
python manage.py runserver


   📁 Project Structure
   animal-shelter/
├── shelter/              # Main project folder
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py
├── animals/              # Main app
│   ├── models.py         # Animal & Adopter models
│   ├── views.py          # CRUD logic
│   ├── forms.py          # Form handling
│   ├── templates/        # HTML templates
│   │   └── animals/
│   └── static/           # CSS & static files
├── media/                # Uploaded animal photos
├── manage.py
└── requirements.txt

⭐ Star this repo if you found it useful!
