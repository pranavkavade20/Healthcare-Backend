
# 🐍 Django Project Setup Guide with Virtual Environment

---

## 📦 Virtual Environment

### ✅ Create a new virtual environment
```bash
python -m venv env_name
```
### ⚙️ Activate virtual environment
- **On Linux or macOS:**
  ```bash
  source env_name/bin/activate
  ```
- **On Windows:**
  ```bash
  .\env_name\Scripts\activate
  ```

### 📥 Install packages
```bash
pip install package_name
```

### 💾 Save installed packages to a file
```bash
# Option 1
pip freeze > requirements.txt

# Option 2
pip list --format=freeze > requirements.txt
```

### 📂 Install packages from a file
```bash
pip install -r requirements.txt
```

### ❌ Deactivate the current virtual environment
```bash
deactivate
```

---

## 🚀 Django Project Commands

### 🛠️ Create Django project
```bash
django-admin startproject project_name
```
---

## 📦 Create Django App
```bash
python manage.py startapp appname
```

### ▶️ Start Django server
```bash
cd project_name
python manage.py runserver
```

### 🗂️ Make migrations for models
```bash
python manage.py makemigrations
python manage.py migrate
```

### 👤 Create a superuser
```bash
python manage.py createsuperuser
```

---

## ⚠️ Hide Development Warning (Optional)

You may see this warning:

> WARNING: This is a development server. Do not use it in a production setting.

To hide it in development:

### 🔧 Add in `settings.py`
```python
import os
os.environ["DJANGO_RUNSERVER_HIDE_WARNING"] = "true"
```

### Or export it temporarily:
```bash
export DJANGO_RUNSERVER_HIDE_WARNING=true
```

---

## 🎨 Static Files (CSS, JS, Images)

### `settings.py`
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

### `urls.py`
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing url patterns ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📄 Templates Setup

### `settings.py` → Inside `TEMPLATES` → `'DIRS'`
```python
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```
---

## 🖼️ Add Support for Image Uploads
To handle images (e.g., for user uploads), install Pillow:
```bash
pip install Pillow
```

---
> ✅ **Tip**: Save this guide as `django_setup_guide.md` and refer back whenever you start a new project.
