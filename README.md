# 🐛 Code Debugging App

A comprehensive Django web application designed for practicing code debugging skills. Users can solve weekly coding challenges while administrators manage content through a dedicated dashboard.

## 🎯 **Core Features**

### **For Users:**
- 🔐 **Individual Accounts** - Personal login with progress tracking
- 📊 **Progress Dashboard** - Track scores, completed challenges, and statistics
- 💻 **Interactive Code Editor** - Built-in Python editor with syntax highlighting
- ▶️ **Code Execution** - Test and run Python code before submitting
- 📈 **Scoring System** - Earn points for each successfully debugged challenge
- 📅 **Week Navigation** - Access previous, current, and upcoming week challenges
- 🎨 **Professional UI** - Modern, responsive design with glass-morphism effects

### **For Administrators:**
- 🎛️ **Admin Dashboard** - Dedicated interface for content management
- 📝 **Challenge Creation** - Upload buggy Python code with expected outputs
- 📊 **Weekly Management** - Organize challenges by weeks with difficulty levels
- 👥 **User Management** - Monitor user progress and submissions
- 🔧 **Content Control** - Full CRUD operations for challenges and weeks

## 🛠️ **Tech Stack**

- **Backend:** Django 5.0, Python 3.x
- **Database:** MySQL 8.0
- **Frontend:** HTML5, CSS3 (Glass-morphism design), JavaScript
- **Code Editor:** Monaco Editor (VS Code editor)
- **Authentication:** Django built-in authentication system
- **Styling:** Custom CSS with responsive design

## 📋 **Prerequisites**

- Python 3.8+
- MySQL 8.0+
- Git

## ⚡ **Quick Start**

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/Code-Debugging-App.git
cd Code-Debugging-App
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **3. Install Dependencies**
```bash
pip install django mysqlclient django-crispy-forms crispy-bootstrap4
```

### **4. Database Setup**
```sql
-- In MySQL Workbench or command line:
CREATE DATABASE code_debugging_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **5. Configure Database**
Update `code_debugging_app/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'code_debugging_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### **6. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **7. Create Superuser**
```bash
python manage.py createsuperuser
```

### **8. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 **Application URLs**

| Page | URL | Description |
|------|-----|-------------|
| **Home** | `http://127.0.0.1:8000/` | Landing page |
| **User Login** | `http://127.0.0.1:8000/auth/login/` | User authentication |
| **User Register** | `http://127.0.0.1:8000/auth/register/` | New user registration |
| **User Dashboard** | `http://127.0.0.1:8000/dashboard/user/` | User progress dashboard |
| **Admin Dashboard** | `http://127.0.0.1:8000/dashboard/admin/` | Admin content management |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | Django admin panel |
| **Week Challenges** | `http://127.0.0.1:8000/challenges/week/<id>/` | Weekly challenges |
| **Challenge Detail** | `http://127.0.0.1:8000/challenges/challenge/<id>/` | Individual challenge |

## 📁 **Project Structure**

```
Code-Debugging-App/
├── code_debugging_app/          # Main Django project
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── authentication/              # User authentication app
│   ├── models.py                # Custom user model
│   ├── views.py                 # Auth views (login/register)
│   └── forms.py                 # Authentication forms
├── challenges/                  # Challenge management app
│   ├── models.py                # Week and Challenge models
│   ├── views.py                 # Challenge views
│   └── admin.py                 # Admin interface
├── dashboard/                   # Dashboard app
│   ├── views.py                 # User and admin dashboards
│   └── urls.py                  # Dashboard URLs
├── templates/                   # HTML templates
│   ├── base.html                # Base template
│   ├── auth/                    # Authentication templates
│   ├── dashboard/               # Dashboard templates
│   └── challenges/              # Challenge templates
├── static/                      # Static files
│   ├── css/                     # Custom CSS
│   └── js/                      # JavaScript files
├── media/                       # User uploads (gitignored)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 💾 **Database Models**

### **User Model (Custom)**
- `username`, `email`, `password`
- `user_type` (admin/user)
- `total_points`, `created_at`

### **Week Model**
- `week_number`, `title`, `description`
- `start_date`, `end_date`
- `is_active`

### **Challenge Model**
- `title`, `description`, `buggy_code`
- `expected_output`, `difficulty`
- `points`, `order`, `week` (ForeignKey)

### **UserSubmission Model**
- `user`, `challenge` (ForeignKeys)
- `submitted_code`, `is_correct`
- `points_earned`, `submitted_at`

## 🎮 **How to Use**

### **As Administrator:**
1. Login with superuser credentials
2. Access admin dashboard at `/dashboard/admin/`
3. Create new weeks using "Create New Week"
4. Add challenges to each week with:
   - Buggy Python code
   - Expected output
   - Difficulty level and points
5. Monitor user progress and submissions

### **As User:**
1. Register a new account at `/auth/register/`
2. Login and access user dashboard
3. View available weeks and challenges
4. Click on challenges to open the code editor
5. Debug the code and test with "Run Code"
6. Submit solution when output matches expected result
7. Track progress and earn points

## 🔧 **Key Features Explained**

### **Code Editor System**
- **Monaco Editor** integration for professional code editing
- **Syntax highlighting** for Python
- **Real-time execution** with output display
- **Fullscreen mode** for better coding experience
- **Auto-save** and **reset** functionality

### **Scoring System**
- Points awarded based on challenge difficulty
- **Easy:** 1 point, **Medium:** 2 points, **Hard:** 3 points
- Progressive scoring with weekly totals
- **Read-only mode** for completed challenges

## 🚀 **Deployment Considerations**

### **Production Settings**
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 👨‍💻 **Developer**

**Sri** - Embedded engineer and ML .
- GitHub: [@Srishanth-023](https://github.com/Srishanth-023)
- Email: your.email@example.com

## 🙏 **Acknowledgments**

- Django Framework for robust backend
- Monaco Editor for professional code editing
- MySQL for reliable data storage
- Bootstrap for responsive design components

---


**📊 Project Status:** Still building...