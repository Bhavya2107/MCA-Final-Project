# Contact App - Documentation

## Table of Contents
1. [App Overview](#app-overview)
2. [File Structure](#file-structure)
3. [Models](#models)
4. [Forms](#forms)
5. [Views](#views)
6. [URLs](#urls)
7. [Admin](#admin)
8. [Templates](#templates)
9. [Email System](#email-system)
10. [Configuration](#configuration)
11. [Usage](#usage)

---

## App Overview

**App Name:** contact  
**Purpose:** Handle customer inquiries, contact form submissions, and email notifications  
**Django Version:** 6.0.4  
**Location:** `c:\Users\sulap\Desktop\Data Transfer\Website\contact\`

---

## File Structure

```
contact/
├── __init__.py          # Empty file (required for Python package)
├── admin.py             # Django admin configuration
├── apps.py              # App configuration
├── forms.py             # Form definitions
├── models.py            # Database models
├── urls.py              # URL routing
├── views.py             # View functions
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py  # Initial migration
├── templates/
│   └── contact/
│       └── contact.html # Contact page template
└── templatetags/
    ├── __init__.py
    └── admin_extras.py  # Custom template tags
```

---

## Models

### File: `contact/models.py`

#### 1. Inquiry Model
Represents a customer inquiry submitted through the contact form.

```python
class Inquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    product = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Fields:**
| Field | Type | Max Length | Required | Description |
|-------|------|------------|----------|-------------|
| `name` | CharField | 120 | Yes | Customer's full name |
| `email` | EmailField | - | Yes | Customer's email address |
| `phone` | CharField | 30 | No | Customer's phone number |
| `message` | TextField | - | Yes | Customer's message |
| `product` | CharField | 200 | No | Product user is inquiring about |
| `created_at` | DateTimeField | - | Auto | Timestamp when inquiry was created |

**Methods:**
- `__str__()`: Returns `"Inquiry from {name} - {email}"`

---

#### 2. ContactInfo Model
Stores business contact information displayed on the contact page.

```python
class ContactInfo(models.Model):
    business_name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    map_embed = models.TextField(blank=True, help_text='Put iframe/embed HTML for map')
```

**Fields:**
| Field | Type | Max Length | Required | Description |
|-------|------|------------|----------|-------------|
| `business_name` | CharField | 200 | Yes | Business name |
| `address` | TextField | - | No | Business address |
| `phone` | CharField | 50 | No | Business phone number |
| `email` | EmailField | - | No | Business email (used for owner notifications) |
| `map_embed` | TextField | - | No | Google Maps iframe HTML |

**Methods:**
- `__str__()`: Returns the business name

---

## Forms

### File: `contact/forms.py`

```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    message = forms.CharField(widget=forms.Textarea)
    product = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
```

**Fields:**
| Field | Widget | Max Length | Required | Validation |
|-------|--------|------------|----------|------------|
| `name` | TextInput | 120 | Yes | CharField validation |
| `email` | EmailInput | - | Yes | EmailField validation |
| `phone` | TextInput | 30 | No | CharField validation |
| `message` | Textarea | - | Yes | Required, no max length |
| `product` | HiddenInput | 200 | No | Hidden field for pre-filling from product pages |

**Notes:**
- The `product` field is hidden and pre-filled via URL query parameter (`?product=Product+Name`)
- Used when users click "Contact" from product detail pages

---

## Views

### File: `contact/views.py`

#### `contact_page(request)`

**Purpose:** Display contact page and handle form submissions

**URL:** `/contact/` (root path)

**Process Flow:**

1. **GET Request (Display Contact Page):**
   - Fetches `ContactInfo` from database (first record)
   - Checks for `?product=` query parameter to pre-fill product field
   - Creates form with initial data if product is specified
   - Renders `contact/contact.html` template

2. **POST Request (Form Submission):**
   - Validates form data
   - Creates `Inquiry` record in database
   - Sends HTML confirmation email to user
   - Sends HTML notification email to site owner (if ContactInfo email exists)
   - Shows success message via Django messages framework
   - Redirects to contact page

**Context Variables Passed to Template:**
| Variable | Type | Description |
|----------|------|-------------|
| `info` | ContactInfo or None | Business contact information |
| `form` | ContactForm | The contact form instance |
| `product_value` | str | Pre-filled product value (if any) |

**Email Features:**
- Uses `EmailMultiAlternatives` for HTML emails
- Sends confirmation email to user with styled HTML template
- Sends notification email to business owner
- Includes fallback if email sending fails (inquiry still saved)

---

## URLs

### File: `contact/urls.py`

```python
app_name = 'contact'

urlpatterns = [
    path('', views.contact_page, name='contact_page'),
]
```

**URL Pattern:**
| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `''` (empty) | `views.contact_page` | `contact_page` | Contact page root URL |

**Usage in templates:**
```html
<a href="{% url 'contact:contact_page' %}">Contact</a>
```

---

## Admin

### File: `contact/admin.py`

#### InquiryAdmin

```python
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'product')
    list_filter = ('created_at',)
    actions = ('export_as_csv',)
```

**Admin Features:**
| Feature | Configuration |
|---------|---------------|
| List Display | name, email, phone, product, created_at |
| Readonly Fields | created_at |
| Search Fields | name, email, product |
| List Filter | created_at |
| Actions | export_as_csv |

**Custom Action: `export_as_csv`**
- Exports selected inquiries to CSV file
- Fields included: name, email, phone, product, message, created_at
- Filename: `inquiries.csv`

**Note:** ContactInfo is not registered in admin by default.

---

## Templates

### File: `contact/templates/contact/contact.html`

**Extends:** `base.html`

**Features:**

1. **Hero Section**
   - Title: "Get In Touch"
   - Subtitle with business description
   - Animated dot grid background
   - Cyan accent color scheme

2. **Info Cards Row**
   - Phone card with click-to-call link
   - Email card with mailto link
   - Address card
   - Business hours display

3. **Contact Form**
   - Full Name field (required)
   - Email field (required)
   - Phone field (optional)
   - Message textarea (required)
   - Product field (hidden, auto-filled from URL)
   - Submit button with loading state

4. **Side Panel**
   - Business hours with status indicators (open/closed)
   - Social media links (Facebook, Twitter, Instagram, LinkedIn)
   - Google Maps embed

5. **Success Toast**
   - Auto-dismisses after 5 seconds
   - Manual close button

**CSS Variables Used:**
```css
:root {
  --primary:       #050c18;
  --primary-soft:  #0a1628;
  --card-bg:       #0d1f35;
  --card-bg2:      #0f2440;
  --accent:        #06b6d4;
  --accent-dark:   #0891b2;
  --accent-glow:   rgba(6,182,212,0.18);
  --accent-border: rgba(6,182,212,0.2);
  --text-primary:  #f0f9ff;
  --text-secondary:#94a3b8;
  --text-muted:    #64748b;
  --red:           #f87171;
  --green:         #34d399;
  --r:             16px;
  --r-sm:          10px;
}
```

**JavaScript Features:**
- Form input class cleanup
- Toast auto-close (5 seconds)
- Submit button loading state ("Sending...")

---

## Email System

### Email Configuration

**File:** `Website/settings.py`

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Email Types

#### 1. User Confirmation Email
**Subject:** "We received your inquiry — Computer & CCTV Hub"

**Features:**
- Gradient dark blue header (#0f2d5e)
- Checkmark badge showing "Inquiry received"
- Inquiry summary card with styled rows
- Message box with blue left border
- Responsive design for mobile
- Footer with brand info

**HTML Structure:**
```html
<div class="wrap">
  <div class="head">
    <!-- Logo and badge -->
  </div>
  <div class="body">
    <!-- Greeting, intro, card, message -->
  </div>
  <div class="foot">
    <!-- Footer info -->
  </div>
</div>
```

#### 2. Owner Notification Email
**Subject:** "New Contact Inquiry - {customer_name}"

**Features:**
- Red gradient header for alert effect
- "NEW MESSAGE" badge
- Full inquiry details in card format
- Yellow warning-style message box

---

## Configuration

### App Registration

**File:** `Website/settings.py`

```python
INSTALLED_APPS = [
    # ... other apps
    'contact',
]
```

### URL Configuration

**File:** `Website/urls.py`

```python
urlpatterns = [
    # ... other urls
    path('contact/', include('contact.urls')),
]
```

### Email Setup (Gmail)

1. Enable **2-Factor Authentication** on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an **App Password** (16 characters)
4. Update `settings.py`:
   ```python
   EMAIL_HOST_USER = 'your-actual-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 16-char app password
   DEFAULT_FROM_EMAIL = 'your-actual-email@gmail.com'
   ```

---

## Usage

### Accessing the Contact Page

**URL:** `http://127.0.0.1:8000/contact/`

### Pre-filling Product from Product Pages

Add query parameter to contact URL:
```
http://127.0.0.1:8000/contact/?product=Dell+Laptop+Inspiron+15
```

### Managing Inquiries

1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Navigate to **Contact** > **Inquiries**
3. View, search, filter, or export inquiries

### Setting Business Contact Info

1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Add ContactInfo via Django shell:
   ```python
   from contact.models import ContactInfo
   ContactInfo.objects.create(
       business_name='COMPUTER & CCTV HUB',
       address='Your Address',
       phone='+1234567890',
       email='owner@example.com',
       map_embed='<iframe src="..."></iframe>'
   )
   ```

### Testing Email

1. Fill out the contact form
2. Submit the form
3. Check your email for confirmation
4. Check owner email (if configured) for notification

---

## Dependencies

### Django Packages
- `django` (6.0.4)
- `django.contrib.admin`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.core.mail`

### External Resources (CDN)
- Google Fonts: Sora, DM Sans
- Font Awesome (for social icons)

---

## Troubleshooting

### Email Not Sending
1. Check email settings in `settings.py`
2. Verify app password is correct (not regular password)
3. Check spam folder
4. Check server console for errors

### Product Field Not Displaying
1. Ensure URL has `?product=` parameter
2. Check `product_value` is passed to template
3. Verify form initial data is set

### Form Not Submitting
1. Check form validation errors
2. Verify CSRF token is present
3. Check browser console for JavaScript errors

### Map Not Displaying
1. Verify `map_embed` field has valid iframe HTML
2. Check Google Maps embed URL is correct

---

## File Paths Reference

| File | Full Path |
|------|-----------|
| Models | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\models.py` |
| Forms | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\forms.py` |
| Views | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\views.py` |
| URLs | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\urls.py` |
| Admin | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\admin.py` |
| Apps | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\apps.py` |
| Template | `c:\Users\sulap\Desktop\Data Transfer\Website\contact\templates\contact\contact.html` |
| Settings | `c:\Users\sulap\Desktop\Data Transfer\Website\Website\settings.py` |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-29 | Initial documentation created |
| 2026-04-29 | Added HTML email support |
| 2026-04-29 | Added product pre-fill functionality |
| 2026-04-29 | Added CSV export for inquiries |

---

*Document generated on April 29, 2026*