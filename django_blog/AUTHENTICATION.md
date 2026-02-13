# Django Blog Authentication System Documentation

## Overview
The Django Blog platform includes a comprehensive authentication system that allows users to register, login, manage their profiles, and reset passwords securely.

## Features

### 1. User Registration
- **URL:** `/register/`
- **Template:** `blog/register.html`
- **Form:** `CustomUserCreationForm`
- **Fields:**
  - Username (required)
  - First Name (required)
  - Last Name (required)
  - Email (required)
  - Password (with validation)
  - Confirm Password

### 2. User Login
- **URL:** `/login/`
- **Template:** `blog/login.html`
- **Uses Django's built-in LoginView**
- Features "Remember Me" functionality
- Redirects to home page upon successful login

### 3. User Logout
- **URL:** `/logout/`
- **Template:** `blog/logout.html`
- **Uses Django's built-in LogoutView**
- Confirms logout and provides login link

### 4. Profile Management
- **URL:** `/profile/` (authenticated users only)
- **Template:** `blog/profile.html`
- **Features:**
  - View profile information
  - Edit profile details (username, name, email)
  - Upload profile picture
  - Add bio, website, location
  - View post count
  - Change password link

### 5. Public Profile View
- **URL:** `/profile/<username>/`
- **Template:** `blog/profile_view.html`
- **Features:**
  - View any user's public profile
  - See user's posts
  - View bio and other public information

### 6. Password Management
- **Change Password:** `/password-change/`
- **Password Reset:** `/password-reset/`
- **Email-based password reset workflow**

## Security Features

1. **CSRF Protection:** All forms include CSRF tokens
2. **Password Hashing:** Django's PBKDF2 algorithm
3. **Login Required Decorators:** Protect authenticated views
4. **Form Validation:** Client and server-side validation
5. **Secure Session Management:** Django's built-in session security

## Testing Instructions

### Test Registration
1. Navigate to `/register/`
2. Fill in all required fields
3. Submit form
4. Verify redirect to home page with success message
5. Check if user can log in with new credentials

### Test Login
1. Navigate to `/login/`
2. Enter valid credentials
3. Verify redirect to home page
4. Check if user menu appears with username

### Test Profile Update
1. Log in and go to `/profile/`
2. Update profile information
3. Upload a profile picture
4. Submit form
5. Verify changes are saved

### Test Password Change
1. Go to `/password-change/`
2. Enter current password and new password
3. Submit form
4. Verify success message
5. Log out and test new password

### Test Public Profile
1. Click on another user's username
2. Verify profile page displays correctly
3. Check if posts are displayed

## Troubleshooting

### Common Issues

1. **Registration fails:**
   - Check password requirements
   - Ensure email is unique
   - Verify all required fields are filled

2. **Login fails:**
   - Check username and password
   - Ensure account is active
   - Clear browser cache/cookies

3. **Profile picture not uploading:**
   - Check file size (max 2MB recommended)
   - Verify image format (JPEG, PNG)
   - Check MEDIA_URL and MEDIA_ROOT settings

## Dependencies

- Django 3.2+
- Pillow (for image handling)
- Python 3.8+

## Configuration

Add to `settings.py`:
```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Email backend (for password reset)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development only