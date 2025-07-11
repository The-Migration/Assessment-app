# Assessment Management System

A comprehensive Django-based application for managing and administering various assessments for recruitment, employee evaluation, and skills testing. Built with security, scalability, and user experience as core priorities.

## 🚀 Recent Updates & Features

### Latest Improvements (2025)
- **✅ Mobile-Responsive Design**: Fully optimized for mobile devices with proper viewport configuration and touch-friendly interfaces
- **✅ Enhanced Security**: Candidate results are now admin-only with secure access controls
- **✅ Hard Delete Implementation**: Questions now use permanent deletion instead of soft delete for cleaner database management
- **✅ Fixed Delete Functionality**: Resolved delete button issues with improved JavaScript handling and confirmation dialogs
- **✅ Deployment Ready**: Complete deployment configuration for Render and other cloud platforms
- **✅ GitHub Integration**: Full version control setup with proper repository management

### Core Functionality
- **Multi-Type Assessments**: Support for IQ tests, cultural assessments, technical evaluations, and custom assessment types
- **Advanced Question Management**: Multiple question formats with intelligent scoring and permanent deletion
- **Role-Based Access Control**: Secure multi-tier user management system with enhanced candidate restrictions
- **Real-Time Assessment Taking**: Timer-based assessments with auto-save functionality
- **Comprehensive Analytics**: Detailed reporting and performance insights (Admin-only access)
- **Bulk Operations**: Import/export questions and results with enhanced error handling
- **Mobile-First Design**: Fully responsive interface optimized for all device types

### Question Types Supported
- **Multiple Choice Questions (MCQ)**: With configurable options and single correct answer
- **True/False Questions**: Simple binary choice questions
- **Short Answer**: Text-based responses for subjective evaluation

### User Interface
- **Admin Dashboard**: Comprehensive management interface with statistics and quick actions
- **Candidate Portal**: User-friendly assessment interface with progress tracking (results restricted)
- **Mobile-Responsive Design**: Bootstrap 5-based responsive design with proper viewport configuration
- **Touch-Friendly Interface**: Optimized for mobile and tablet interactions
- **Real-Time Features**: Live timer, auto-save, progress indicators
- **Enhanced Delete Functionality**: Improved confirmation dialogs with proper JavaScript handling

## 🔒 Security Features

### Enhanced Security (2025 Updates)
- **Candidate Results Restriction**: Assessment results are now admin-only, candidates see only completion confirmation
- **Secure Result Access**: Moved assessment results to admin-only URLs with proper access controls
- **Enhanced Delete Protection**: Permanent deletion with multiple confirmation layers and impact analysis
- **Improved Session Management**: Better session handling with secure redirects

### Authentication & Authorization
- **Multi-Level Admin Access**: Restricted admin access to authorized email addresses only
- **Role-Based Permissions**: Granular access control (Admin, Candidate, HR)
- **Secure Authentication Backend**: Custom authentication with name-based login for candidates
- **Session Management**: Secure session handling with configurable timeouts
- **Password Security**: Django's built-in password validation and hashing

### Data Protection
- **CSRF Protection**: Cross-Site Request Forgery protection on all forms
- **SQL Injection Prevention**: Django ORM protection against SQL injection attacks
- **XSS Protection**: Cross-Site Scripting prevention through template escaping
- **Input Validation**: Comprehensive server-side validation for all user inputs
- **Secure File Handling**: Safe file upload and processing for bulk imports
- **Hard Delete Security**: Permanent deletion with comprehensive impact warnings

### Access Control
- **Email-Based Authorization**: Admin access restricted to specific authorized email addresses:
  - `zainab.akram@themigration.com.au`
  - `hr@istudywise.com`
  - `nauman@istudywise.com`
  - `careers@themigration.com.au`
  - `sheyral@themigration.com.au`
- **Multi-Layer Security**: View-level, decorator-level, and middleware-level access checks
- **Admin Access Monitoring**: Comprehensive logging and monitoring of admin activities
- **Secure Admin Panel**: Django admin interface with additional security restrictions
- **Candidate Result Isolation**: Complete separation of candidate and admin result access

## 🛠 Technology Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Bootstrap 5, jQuery 3.6, Font Awesome 6
- **Security**: Django's security framework with custom enhancements
- **Deployment**: Render-ready with WhiteNoise, Gunicorn, and PostgreSQL support
- **Additional**: django-crispy-forms, django-import-export, python-decouple, dj-database-url

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/The-Migration/Assessment-app.git
cd assessment_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin Users
```bash
# Create multiple authorized admin users
python manage.py create_multiple_authorized_admins --password admin123

# Or create a specific admin user
python manage.py create_authorized_admin
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🌐 Deployment

### Render Deployment (Recommended)
The application is fully configured for deployment on Render with the following files:

#### Required Files (Included)
- `render.yaml` - One-click deployment configuration
- `build.sh` - Build script for Render
- `requirements.txt` - Production dependencies including PostgreSQL
- `runtime.txt` - Python version specification
- `Procfile` - Alternative deployment method

#### Environment Variables for Render
```env
PYTHON_VERSION=3.11.0
SECRET_KEY=y30@kfi6wj5_92s#4&fv-#z)b8#rwn5+_y9x$!2d^*m*(_3zxl
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

#### Deployment Steps
1. **Push to GitHub**: Code is already in repository
2. **Connect to Render**: Link your GitHub repository
3. **Set Environment Variables**: Configure the variables above
4. **Deploy**: Render will automatically build and deploy
5. **Create Admin User**: Run management command post-deployment

### Alternative Deployment Options
- **Heroku**: Compatible with included Procfile
- **DigitalOcean**: App Platform ready
- **AWS**: Elastic Beanstalk compatible
- **Docker**: Containerization ready

## 🎯 Usage Guide

### Access Points

#### Default Home Page
- **URL**: `http://127.0.0.1:8000/`
- **Description**: Main landing page with options for candidates and admins
- **Mobile**: Fully responsive on all devices

#### Admin Access
- **Custom Admin Login**: `http://127.0.0.1:8000/accounts/admin-login/`
- **Admin Signup**: `http://127.0.0.1:8000/accounts/admin-signup/` (restricted access)
- **Django Admin**: `http://127.0.0.1:8000/admin/`
- **Admin Dashboard**: `http://127.0.0.1:8000/assessments/admin-dashboard/`

#### Candidate Access
- **Candidate Login**: `http://127.0.0.1:8000/accounts/login/`
- **Candidate Portal**: `http://127.0.0.1:8000/assessments/candidate-portal/`
- **Assessment Completion**: Results restricted, only completion confirmation shown

### User Roles & Permissions

#### Admin Users
- **Full System Access**: Complete control over all system functions
- **Assessment Management**: Create, edit, delete assessments with enhanced delete confirmation
- **Question Management**: Manage question bank with permanent deletion capability
- **User Management**: Monitor candidate activities and sessions
- **Analytics Access**: View comprehensive reports and statistics
- **Results Access**: Exclusive access to detailed assessment results
- **Bulk Operations**: Import/export data and perform batch operations

#### Candidate Users
- **Assessment Taking**: Access to assigned assessments
- **Progress Tracking**: View assessment history and completion status
- **Profile Management**: Basic profile information
- **Session Management**: Resume incomplete assessments
- **Restricted Results**: Only see completion confirmation, no detailed scores

### Enhanced Features

#### Mobile Responsiveness
- **Responsive Design**: Optimized for phones, tablets, and desktops
- **Touch Interface**: Touch-friendly buttons and navigation
- **Viewport Optimization**: Proper scaling on all screen sizes
- **Performance**: Fast loading on mobile networks

#### Delete Functionality
- **Hard Delete**: Permanent removal of questions and assessments
- **Confirmation Dialogs**: Multiple confirmation steps with impact analysis
- **JavaScript Enhancement**: Improved delete button functionality with proper error handling
- **Data Protection**: Clear warnings about permanent data loss

#### Security Enhancements
- **Result Isolation**: Complete separation of candidate and admin result access
- **Secure Redirects**: Proper post-action redirects with security validation
- **Enhanced Logging**: Comprehensive activity logging for security monitoring

## 🔧 Key Features in Detail

### Assessment Management
- **Flexible Configuration**: Custom time limits, pass thresholds, attempt limits
- **Question Assignment**: Add/remove questions with custom ordering
- **Bulk Operations**: Import questions from Excel/CSV files
- **Assessment Cloning**: Duplicate assessments for quick setup
- **Status Management**: Active/inactive assessment control
- **Enhanced Delete**: Permanent deletion with comprehensive impact analysis

### Question Management
- **Rich Question Types**: Support for various question formats
- **Smart Validation**: Form validation for question consistency
- **Bulk Import**: Excel/CSV import with error handling
- **Category Organization**: Hierarchical question organization
- **Point System**: Flexible scoring with custom point values
- **Hard Delete**: Permanent question removal with multi-step confirmation

### User Experience
- **Mobile-First Design**: Responsive interface optimized for all devices
- **Real-Time Features**: Live timer, auto-save, progress tracking
- **Accessibility**: WCAG-compliant design elements
- **Intuitive Navigation**: Clear user flows and helpful guidance
- **Enhanced Feedback**: Improved confirmation dialogs and user notifications

### Analytics & Reporting (Admin Only)
- **Performance Metrics**: Score distributions, completion rates, time analysis
- **Comparative Analysis**: Cross-assessment and user comparisons
- **Export Capabilities**: CSV, Excel, and PDF export options
- **Historical Tracking**: Long-term performance trends
- **Secure Access**: Admin-only analytics with proper access controls

## 📊 Database Models

### Core Models

#### CustomUser
- **Purpose**: Extended user model with role-based access
- **Fields**: username, email, first_name, last_name, role, phone, department, employee_id
- **Roles**: 'admin', 'candidate'
- **Security**: Email-based admin authorization with enhanced restrictions

#### Assessment
- **Purpose**: Assessment configuration and metadata
- **Fields**: name, description, assessment_type, time_limit_minutes, pass_threshold, max_attempts
- **Features**: Randomization, retake settings, result display options
- **Delete**: Hard delete with cascade protection

#### Question
- **Purpose**: Question bank with multiple formats
- **Fields**: text, question_type, options, correct_answer, points
- **Types**: MCQ, TF (True/False), SA (Short Answer)
- **Delete**: Hard delete implementation (permanent removal)
- **Note**: `is_active` field exists but not used in queries (legacy field)

#### AssessmentSession
- **Purpose**: Individual assessment attempts tracking
- **Fields**: user, assessment, status, started_at, completed_at, score
- **Security**: User isolation, session validation, admin-only result access

#### Answer
- **Purpose**: User responses to individual questions
- **Fields**: session, question, response, is_correct, points_earned
- **Features**: Automatic scoring, manual review capability

### Supporting Models

#### Designation
- **Purpose**: Assessment categorization (IQ Test, Cultural Assessment, etc.)
- **Usage**: Organizing assessments by type and purpose

#### QuestionCategory
- **Purpose**: Question organization and filtering
- **Usage**: Grouping questions by topic or skill area

#### AssessmentQuestion
- **Purpose**: Many-to-many relationship between assessments and questions
- **Features**: Question ordering, custom point allocation

## 🌐 API Endpoints

### Authentication Endpoints
- `POST /accounts/login/` - Candidate name-based login
- `POST /accounts/admin-login/` - Admin username/password login
- `POST /accounts/admin-signup/` - Restricted admin registration
- `POST /accounts/logout/` - Secure logout with role-based redirects

### Assessment Management (Admin Only)
- `GET /assessments/admin-dashboard/` - Admin dashboard with statistics
- `GET /assessments/admin/assessments/` - Assessment list with filtering
- `POST /assessments/admin/assessments/create/` - Create new assessment
- `GET /assessments/admin/assessments/<id>/` - Assessment details
- `PUT /assessments/admin/assessments/<id>/edit/` - Edit assessment
- `DELETE /assessments/admin/assessments/<id>/delete/` - Delete assessment (hard delete)
- `GET /assessments/admin/questions/` - Question management
- `POST /assessments/admin/questions/create/` - Create questions
- `DELETE /assessments/admin/questions/<id>/delete/` - Delete question (hard delete)
- `GET /assessments/admin/sessions/` - Session monitoring
- `GET /assessments/admin/analytics/` - Performance analytics
- `GET /assessments/admin/assessment-results/<id>/` - View detailed results (Admin only)

### Assessment Taking (Candidate)
- `GET /assessments/candidate-portal/` - Candidate dashboard
- `POST /assessments/start-assessment/<id>/` - Start assessment session
- `GET /assessments/take-assessment/<session_id>/` - Assessment interface
- `POST /assessments/submit-assessment/<session_id>/` - Submit completed assessment
- `GET /assessments/assessment-completed/<session_id>/` - Completion confirmation (Candidate)

### AJAX Endpoints
- `POST /assessments/ajax/save-answer/` - Auto-save answers during assessment

## 🔐 Security Implementation Details

### Enhanced Security Features (2025)
```python
# Candidate result isolation
@admin_required
def assessment_results(request, session_id):
    """Admin-only access to detailed results"""
    # Comprehensive security validation
    
@login_required
@user_passes_test(is_candidate)
def assessment_completed(request, session_id):
    """Candidate completion confirmation only"""
    # No detailed scores or analytics
```

### Hard Delete Implementation
```python
@admin_required
def question_delete(request, question_id):
    """Delete a question permanently"""
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question_text = question.text[:50]
        question.delete()  # Permanent deletion
        messages.success(request, f"Question '{question_text}...' deleted successfully!")
```

### Mobile Responsiveness
```html
<!-- Proper viewport configuration -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Bootstrap 5 responsive classes -->
<div class="container-fluid">
    <div class="row">
        <div class="col-12 col-md-6 col-lg-4">
            <!-- Responsive content -->
        </div>
    </div>
</div>
```

### Authentication Security
```python
# Multiple authentication backends
AUTHENTICATION_BACKENDS = [
    'users.backends.FirstLastNameBackend',  # Candidate name-based auth
    'django.contrib.auth.backends.ModelBackend',  # Admin username/password auth
]

# Authorized admin emails (centrally managed)
AUTHORIZED_ADMIN_EMAILS = [
    'zainab.akram@themigration.com.au',
    'hr@istudywise.com',
    'nauman@istudywise.com',
    'careers@themigration.com.au',
    'sheyral@themigration.com.au'
]
```

## ⚙️ Configuration

### Production Settings (Render Ready)
```python
# Production configuration
import dj_database_url

# Database configuration for PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files with WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
    # ... other middleware
]

# Security headers for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Mobile Optimization
```css
/* Responsive design enhancements */
@media (max-width: 768px) {
    .btn-group {
        flex-direction: column;
        width: 100%;
    }
    
    .table-responsive {
        font-size: 0.875rem;
    }
    
    .card {
        margin-bottom: 1rem;
    }
}
```

## 🧪 Testing

### Enhanced Testing Coverage
```bash
# Run all tests
python manage.py test

# Test specific functionality
python manage.py test assessments.tests.test_delete_functionality
python manage.py test assessments.tests.test_mobile_responsiveness
python manage.py test assessments.tests.test_security_restrictions

# Security testing
python manage.py test assessments.tests.test_candidate_result_isolation
```

### Mobile Testing
- **Responsive Design**: Test on various screen sizes
- **Touch Interface**: Verify touch-friendly interactions
- **Performance**: Mobile network performance testing
- **Cross-Browser**: Testing on mobile browsers

## 🔄 Management Commands

### Enhanced User Management
```bash
# Create authorized admin users with enhanced security
python manage.py create_multiple_authorized_admins

# Clean up and optimize database
python manage.py cleanup_duplicate_users

# Create specific admin user with proper validation
python manage.py create_authorized_admin
```

### Deployment Commands
```bash
# Production deployment
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py create_multiple_authorized_admins --password=secure_admin_password
```

## 🚀 Deployment Guide

### Render Deployment Steps

1. **GitHub Repository**: Code is already pushed to https://github.com/The-Migration/Assessment-app.git

2. **Render Setup**:
   - Connect GitHub repository to Render
   - Use `render.yaml` for one-click deployment
   - Set environment variables:
     ```
     PYTHON_VERSION=3.11.0
     SECRET_KEY=y30@kfi6wj5_92s#4&fv-#z)b8#rwn5+_y9x$!2d^*m*(_3zxl
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.onrender.com
     ```

3. **Build Configuration**:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn assessment_web.wsgi:application`

4. **Post-Deployment**:
   ```bash
   # Create admin users
   python manage.py create_multiple_authorized_admins
   
   # Verify deployment
   python manage.py check --deploy
   ```

### Environment Variables
```env
# Production Configuration
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname

# Security Settings
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

## 📱 Mobile Features

### Responsive Design
- **Bootstrap 5**: Mobile-first responsive framework
- **Viewport Configuration**: Proper meta viewport settings
- **Touch Interface**: Optimized for touch interactions
- **Performance**: Fast loading on mobile networks

### Mobile-Specific Features
- **Touch-Friendly Buttons**: Larger touch targets
- **Swipe Navigation**: Enhanced mobile navigation
- **Responsive Tables**: Horizontal scrolling for data tables
- **Mobile Forms**: Optimized form layouts for mobile

## 🔒 Security Updates

### Candidate Result Restrictions
- **Admin-Only Results**: Detailed results accessible only to admins
- **Completion Confirmation**: Candidates see only completion status
- **Secure URLs**: Results moved to admin-only URL patterns
- **Session Isolation**: Complete separation of candidate and admin sessions

### Hard Delete Implementation
- **Permanent Deletion**: Questions and assessments are permanently removed
- **Impact Analysis**: Comprehensive warnings about deletion consequences
- **Confirmation Dialogs**: Multiple confirmation steps
- **Data Loss Prevention**: Clear warnings about irreversible actions

## 🤝 Contributing

### Development Guidelines
- Follow Django best practices
- Maintain mobile responsiveness
- Ensure security standards
- Add tests for new features
- Update documentation
- Follow PEP 8 coding standards

### Security Considerations
- Always test candidate result isolation
- Verify admin-only access controls
- Test mobile responsiveness
- Validate delete functionality
- Check deployment configurations

## 📝 Recent Changes Log

### Version 2025.1
- ✅ **Mobile Responsiveness**: Complete mobile optimization
- ✅ **Security Enhancement**: Candidate result restrictions
- ✅ **Hard Delete**: Permanent deletion implementation
- ✅ **Delete Button Fix**: Resolved JavaScript and confirmation issues
- ✅ **Deployment Ready**: Full Render deployment configuration
- ✅ **GitHub Integration**: Version control and repository setup

### Previous Versions
- Authentication system with role-based access
- Assessment and question management
- Real-time assessment taking
- Analytics and reporting
- Bulk import/export functionality

## 📞 Support & Documentation

### Getting Help
- **Repository**: https://github.com/The-Migration/Assessment-app
- **Issues**: Report bugs via GitHub Issues
- **Security**: Report security issues privately
- **Documentation**: Comprehensive inline documentation

### System Requirements
- **Development**: Python 3.8+, 2GB RAM, 1GB storage
- **Production**: Python 3.11+, 4GB RAM, 5GB storage, PostgreSQL
- **Mobile**: Responsive on all modern mobile browsers

---

**Assessment Management System** - Secure, Mobile-Responsive, Production-Ready Assessment Platform  
Built with ❤️ using Django and modern web technologies.

*Last Updated: January 2025 - Version 2025.1*
