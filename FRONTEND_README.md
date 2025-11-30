# Healthcare System - Modern Frontend

A modern, responsive Django frontend for the Healthcare Management System using Tailwind CSS, Alpine.js, and Font Awesome icons.

## Features

### 🎨 Modern Design
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Interactive Components** - Alpine.js for lightweight interactivity
- **Font Awesome Icons** - Beautiful icon library

### 👥 Patient Management
- **Patient List** - Browse all patients with search and filter capabilities
- **Patient Details** - Comprehensive patient information display
- **Add/Edit Patient** - Full-featured forms for creating and updating patient records
- **Delete Patient** - Safe deletion with confirmation
- **Medical History** - Track medical conditions, allergies, and medications

### 👨‍⚕️ Doctor Management
- **Doctor List** - Grid/card view of doctors with quick information
- **Doctor Details** - Detailed doctor profile with specialization and availability
- **Add/Edit Doctor** - Complete doctor registration forms
- **Delete Doctor** - Safe doctor removal
- **Filter by Specialization** - Find doctors by specialty and location

### 🔗 Mappings/Assignments
- **Create Assignments** - Link patients with doctors
- **View All Assignments** - See all patient-doctor mappings
- **Manage Status** - Track assignment status (Active, Inactive, Completed)
- **Quick Access** - Easy access to related patient/doctor details

### 📊 Dashboard
- **Statistics Cards** - Quick overview of patients, doctors, and assignments
- **Quick Actions** - Fast access to create new records
- **Recent Activity** - See recent system activities
- **System Health** - Monitor system status

### 🔐 Authentication
- **User Registration** - Create new accounts
- **Login** - Secure user authentication
- **Logout** - Session management
- **Profile** - User profile management
- **Settings** - User preferences

## Directory Structure

```
healthcare/
├── templates/
│   ├── base.html                          # Main template with navigation
│   ├── authentication/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── settings.html
│   ├── healthcare/
│   │   └── dashboard.html
│   ├── patients/
│   │   ├── patient_list.html
│   │   ├── patient_detail.html
│   │   ├── patient_form.html
│   │   └── patient_confirm_delete.html
│   ├── doctors/
│   │   ├── doctor_list.html
│   │   ├── doctor_detail.html
│   │   ├── doctor_form.html
│   │   └── doctor_confirm_delete.html
│   └── mappings/
│       ├── mapping_list.html
│       ├── mapping_form.html
│       └── mapping_confirm_delete.html
├── static/
│   ├── css/
│   │   └── style.css                     # Custom CSS styles
│   ├── js/
│   │   └── main.js                       # Main JavaScript
│   └── images/
├── frontend_views.py                      # Frontend view functions
├── frontend_urls.py                       # Frontend URL routing
└── ...
```

## Installation & Setup

### Step 1: Update Django Settings

The frontend is automatically configured in `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Step 2: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## URL Routes

### Authentication
- `http://127.0.0.1:8000/auth/register/` - Registration
- `http://127.0.0.1:8000/auth/login/` - Login
- `http://127.0.0.1:8000/auth/logout/` - Logout
- `http://127.0.0.1:8000/auth/profile/` - User Profile
- `http://127.0.0.1:8000/auth/settings/` - Settings

### Dashboard & Home
- `http://127.0.0.1:8000/` - Dashboard (requires login)
- `http://127.0.0.1:8000/dashboard/` - Dashboard

### Patients
- `http://127.0.0.1:8000/patients/` - Patient List
- `http://127.0.0.1:8000/patients/<id>/` - Patient Detail
- `http://127.0.0.1:8000/patients/create/` - Create Patient
- `http://127.0.0.1:8000/patients/<id>/edit/` - Edit Patient
- `http://127.0.0.1:8000/patients/<id>/delete/` - Delete Patient

### Doctors
- `http://127.0.0.1:8000/doctors/` - Doctor List
- `http://127.0.0.1:8000/doctors/<id>/` - Doctor Detail
- `http://127.0.0.1:8000/doctors/create/` - Create Doctor
- `http://127.0.0.1:8000/doctors/<id>/edit/` - Edit Doctor
- `http://127.0.0.1:8000/doctors/<id>/delete/` - Delete Doctor

### Mappings
- `http://127.0.0.1:8000/mappings/` - Mapping List
- `http://127.0.0.1:8000/mappings/create/` - Create Mapping
- `http://127.0.0.1:8000/mappings/<id>/edit/` - Edit Mapping
- `http://127.0.0.1:8000/mappings/<id>/delete/` - Delete Mapping

## Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS v3** - Utility-first CSS framework (CDN)
- **Alpine.js v3** - Lightweight JavaScript framework
- **Font Awesome 6.4** - Icon library

### Backend
- **Django 5.2** - Web framework
- **Django Templates** - Server-side rendering
- **PostgreSQL** - Database (from API)

## Features Details

### Search & Filtering

**Patients:**
- Search by name, phone, or email
- Filter by gender
- Filter by city
- Pagination support

**Doctors:**
- Search by name, specialization, or city
- Filter by specialization
- Filter by city
- Grid view with cards
- Pagination support

**Mappings:**
- Search by patient or doctor name
- Filter by status (Active, Inactive, Completed)
- Pagination support

### Forms

All forms include:
- Client-side validation
- Required field indicators
- Error messages
- Success notifications
- Cancel buttons
- Responsive layout

### Dashboard

Statistics cards showing:
- Total active patients
- Total available doctors
- Total active assignments
- System status

Quick actions for:
- Adding new patient
- Adding new doctor
- Creating new assignment

### Navigation

- Top navigation bar with user menu
- Active page highlighting
- Mobile-responsive hamburger menu
- Quick links to main sections
- User profile dropdown

## Customization

### Colors

Edit Tailwind color classes:
- Blue (`-blue-`) - Primary actions (patients)
- Green (`-green-`) - Secondary actions (doctors)
- Purple (`-purple-`) - Tertiary actions (mappings)
- Red (`-red-`) - Danger actions (delete)
- Yellow (`-yellow-`) - Warnings
- Gray (`-gray-`) - Neutral elements

### Styling

Modify `static/css/style.css` for:
- Custom animations
- Additional utilities
- Component-specific styles
- Print styles

### JavaScript

Update `static/js/main.js` for:
- Form validation rules
- API integrations
- Custom interactions
- Utility functions

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance

- Lazy loading of images (placeholder)
- Optimized CSS with Tailwind
- Minimal JavaScript dependencies
- Responsive images
- CSS animations instead of JavaScript

## Security

- CSRF protection (Django templates)
- Login required decorators
- User isolation (own data only)
- SQL injection protection
- XSS protection

## API Integration

The frontend can be integrated with the existing API:

```javascript
// Example API call
fetch('/api/patients/', {
    headers: {
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
# In settings.py, ensure DEBUG = True in development
```

### Templates not found
```bash
# Check TEMPLATES dirs in settings.py
# Ensure templates folder exists at project root
```

### CSS not working
- Clear browser cache (Ctrl+Shift+Delete)
- Run collectstatic again
- Check STATIC_URL and STATIC_ROOT in settings.py

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Export to PDF
- [ ] Print functionality
- [ ] Advanced search with date ranges
- [ ] Appointment scheduling
- [ ] Medical reports
- [ ] Email notifications
- [ ] SMS alerts
- [ ] File uploads
- [ ] Multi-language support

## License

This project is part of the Healthcare Backend System assignment.

## Support

For issues or questions, please refer to the main README.md in the project root.
