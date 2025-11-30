# Frontend Setup Instructions

## Quick Start Guide

Follow these steps to set up and run the modern frontend for the Healthcare System.

### Prerequisites

- Python 3.8+
- Django 5.2
- PostgreSQL database (configured in your .env file)
- Virtual environment activated

### Step-by-Step Setup

#### 1. Verify Django Installation

```bash
python manage.py --version
# Should show: Django 5.2.x
```

#### 2. Run Database Migrations

```bash
cd healthcare
python manage.py migrate
```

#### 3. Create Superuser Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 4. Collect Static Files (Production)

For development, this is optional but recommended:

```bash
python manage.py collectstatic --noinput
```

#### 5. Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

#### 6. Access the Application

Open your browser and navigate to:

**Frontend (Recommended):**
- http://127.0.0.1:8000/ - Main dashboard
- http://127.0.0.1:8000/auth/login/ - Login page

**Admin Panel:**
- http://127.0.0.1:8000/admin/ - Django admin

### First Time Usage

1. **Register an Account**
   - Go to http://127.0.0.1:8000/auth/register/
   - Create a new account with your email
   - You'll be redirected to login page

2. **Login**
   - Use your registered credentials
   - You'll be directed to the dashboard

3. **Create Sample Data**
   - Click "Add Patient" to create your first patient
   - Click "Add Doctor" to add a doctor
   - Create an assignment linking them together

4. **Explore Features**
   - Browse the patient and doctor lists
   - View detailed profiles
   - Edit and delete records
   - Create multiple assignments

### Frontend Pages Overview

#### Dashboard (`/`)
- Statistics overview
- Quick action buttons
- Recent activity
- System status

#### Patients (`/patients/`)
- **List View**: Browse all patients with search/filter
- **Detail View**: See complete patient information
- **Create**: Add new patient with all medical details
- **Edit**: Update patient information
- **Delete**: Remove patient with confirmation

#### Doctors (`/doctors/`)
- **List View**: Grid view of doctors
- **Detail View**: Complete doctor profile
- **Create**: Register new doctor
- **Edit**: Update doctor details
- **Delete**: Remove doctor with confirmation

#### Mappings (`/mappings/`)
- **List View**: All patient-doctor assignments
- **Create**: Link patient with doctor
- **Edit**: Update assignment status
- **Delete**: Remove assignment

#### Authentication
- **Register** (`/auth/register/`): Create new account
- **Login** (`/auth/login/`): Sign in to system
- **Logout** (`/auth/logout/`): Sign out
- **Profile** (`/auth/profile/`): View user profile
- **Settings** (`/auth/settings/`): User preferences

### Features & Shortcuts

#### Search
- Patient list: Search by name, phone, email
- Doctor list: Search by name, specialization, city
- Mapping list: Search by patient or doctor name

#### Filters
- Patient: Gender, City
- Doctor: Specialization, City
- Mapping: Status (Active/Inactive/Completed)

#### Keyboard Shortcuts (Future)
- `Ctrl+/` - Command palette
- `Ctrl+K` - Search
- `Ctrl+D` - Dashboard

### Configuration

#### Update Django Settings (Already Done)

The settings have been configured in `healthcare/settings.py`:

```python
# Templates directory
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### Environment Variables (.env)

Ensure your `.env` file contains:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Customization

#### Change Application Title

Edit `templates/base.html`:
```html
<span class="text-xl font-bold text-gray-800">Your App Name</span>
```

#### Modify Colors

Edit `static/css/style.css`:
```css
:root {
    --color-primary: #YOUR_COLOR;
    --color-secondary: #YOUR_COLOR;
}
```

Or use Tailwind classes directly in templates:
- Blue (`-blue-600`, `-blue-700`) for primary
- Green (`-green-600`, `-green-700`) for secondary
- Purple (`-purple-600`, `-purple-700`) for tertiary

#### Add New Pages

1. Create template in `templates/app_name/`
2. Create view function in `healthcare/frontend_views.py`
3. Add URL pattern in `healthcare/frontend_urls.py`

### Troubleshooting

#### Issue: "TemplateDoesNotExist"
```
Solution:
- Check TEMPLATES 'DIRS' in settings.py
- Ensure templates folder exists at project root
- Verify file names match the template path
```

#### Issue: "Static files not loading"
```
Solution:
python manage.py collectstatic --noinput
# Clear browser cache (Ctrl+Shift+Delete)
```

#### Issue: "Login required but not working"
```
Solution:
- Check LOGIN_URL setting
- Verify @login_required decorators on views
- Clear browser cookies
```

#### Issue: "Database not found"
```
Solution:
- Check .env file DATABASE settings
- Run: python manage.py migrate
- Ensure PostgreSQL is running
```

### Development Tips

1. **Hot Reload**: Django automatically reloads on file changes
2. **Debug Mode**: Set `DEBUG=True` in .env for detailed error pages
3. **Database Shell**: `python manage.py dbshell` for SQL queries
4. **Django Shell**: `python manage.py shell` for Python REPL

### Performance Tips

1. **Pagination**: Lists are paginated (10-12 items per page)
2. **Caching**: Consider adding caching for frequently accessed data
3. **Indexing**: Database indexes are already added to models
4. **CDN**: Tailwind and Alpine.js use CDN for performance

### Security Reminders

1. Never commit `.env` file
2. Use strong SECRET_KEY
3. Set DEBUG=False in production
4. Always validate user input
5. Use HTTPS in production
6. Keep Django updated

### Next Steps

1. **Customize**: Add your own styles and features
2. **Deploy**: Set up production server
3. **Test**: Write tests for views and forms
4. **Monitor**: Set up error logging and monitoring
5. **Scale**: Consider load balancing for high traffic

### Support & Documentation

- Django Docs: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- Alpine.js: https://alpinejs.dev/
- Font Awesome: https://fontawesome.com/

### Common Commands

```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Access Django shell
python manage.py shell

# Access database
python manage.py dbshell

# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Check for issues
python manage.py check
```

### File Structure Reference

```
healthcare_backend/
├── healthcare/               # Main project folder
│   ├── manage.py            # Django management script
│   ├── templates/           # Django templates (HTML)
│   │   ├── base.html       # Main template
│   │   ├── authentication/
│   │   ├── patients/
│   │   ├── doctors/
│   │   └── mappings/
│   ├── static/              # Static files (CSS, JS, Images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── healthcare/
│   │   ├── settings.py     # Settings configuration
│   │   ├── urls.py         # Main URL configuration
│   │   ├── frontend_views.py  # Frontend view functions
│   │   └── frontend_urls.py   # Frontend URL routing
│   ├── authentication/      # Auth app
│   ├── patients/            # Patient app
│   ├── doctors/             # Doctor app
│   └── mappings/            # Mapping app
├── FRONTEND_README.md       # Frontend documentation
└── requirements.txt         # Python dependencies
```

### Complete Feature List

✅ **Implemented:**
- Modern responsive UI with Tailwind CSS
- Patient management (CRUD)
- Doctor management (CRUD)
- Mappings/Assignments (CRUD)
- User authentication (Register/Login/Logout)
- Search and filtering
- Dashboard with statistics
- Navigation and user menu
- Form validation
- Error handling
- Success messages
- Pagination
- Responsive design (Mobile/Tablet/Desktop)

🔜 **Future Enhancements:**
- Dark mode
- Export to PDF/CSV
- Print functionality
- Appointment scheduling
- Medical reports
- File uploads
- Email notifications
- SMS alerts
- Advanced analytics
- Multi-language support

---

**Enjoy using the Healthcare Management System!**

For any questions or issues, refer to the main project README.md
