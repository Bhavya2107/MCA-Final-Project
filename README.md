# COMPUTER & CCTV HUB

> A polished Django marketplace for laptops, accessories, support, and orders.

---

## ✨ Project Overview

**COMPUTER & CCTV HUB** is a designer-style Django e-commerce platform created to manage electronics, laptops, accessories, and customer service requests.

This repository includes the `Website` Django project and six main feature apps:

| App | Role |
| --- | --- |
| `accounts` | Registration, login, OTP verification, password recovery, and user profiles |
| `accessories` | Accessories catalog with categories, filters, product details, and inquiries |
| `used_laptops` | Used laptop listings, categories, detailed specs, and inquiries |
| `cart` | Cart management, checkout, delivery address, and order processing |
| `contact` | Contact page, inquiry handling, email notifications, and business info |
| `new_laptops` | Request a laptop workflow, request tracking, and notification emails |

---

## 🧩 Experience Highlights

### ✅ Secure User Journey

- Email + phone registration
- OTP verification before account activation
- Login with username or email
- Password reset links
- Profile view/edit and password change

### 🛒 Modern Shopping Flow

- Product categories and dynamic filtering
- Product detail pages with inquiry capture
- Add items from multiple apps to one shared cart
- GST automatically calculated at **18%**
- Delivery pricing logic based on location
- Smooth checkout with order confirmation

### 📬 Contact & Support

- Contact page with configurable business information
- Inquiry submissions saved in the database
- Admin-friendly CSV export of inquiries
- Notification emails for support actions

### 💼 Laptop Request Workflow

- User request form for unavailable laptops
- Request tracking for customers and admins
- Notifications sent to users and owner
- Admin workflow for pending/completed/rejected statuses

---

## 📁 Structure Overview

```
Website/
  manage.py
  db.sqlite3
  requirements.txt
  static/
  media/
  templates/
  accounts/
  accessories/
  cart/
  contact/
  new_laptops/
  used_laptops/
```

### Important Files

- `manage.py` — Django project entrypoint
- `Website/settings.py` — configuration for app, static, media, email, i18n
- `Website/urls.py` — site routing
- `requirements.txt` — dependency list
- `templates/` — shared HTML templates
- `media/` — uploaded images and files

---

## 📦 Dependencies

The project uses:

- `Django==6.0.4`
- `pillow==12.2.0`
- `asgiref==3.11.1`
- `sqlparse==0.5.5`
- `tzdata==2026.1`

> Note: Twilio is referenced in the code for SMS OTP but is not installed by default.

---

## ⚙️ Configuration

### Database

- Default engine: SQLite (`db.sqlite3`)

### Static & Media

- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`

### Localization

- Default language: `en-us`
- Supported languages: `English`, `Thai (ไทย)`
- Locale path: `BASE_DIR / 'locale'`

### Email

- Default backend: `console.EmailBackend`
- SMTP settings are available but commented out
- Recommended env vars:
  - `EMAIL_HOST_USER`
  - `EMAIL_HOST_PASSWORD`
  - `NEW_LAPTOP_REQUEST_NOTIFICATION_EMAIL`

### SMS OTP

- Optional Twilio support uses:
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_PHONE_NUMBER`

If Twilio is absent, OTP codes are logged for development.

### Security

- `DEBUG = True` for local development
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`
- Dev-friendly CSRF/session cookie settings
- Secure headers for XSS and MIME sniffing enabled

---

## 🌐 Site Pages

### Core Pages

- `/` — Home
- `/about/` — About
- `/privacy/` — Privacy policy
- `/terms/` — Terms
- `/developer/` — Developer page

### Account Pages

- `/accounts/register/`
- `/accounts/verify-otp/<user_id>/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/forgot-password/`
- `/accounts/reset-password/<token>/`
- `/accounts/profile/`
- `/accounts/profile/edit/`
- `/accounts/change-password/`

### Product Pages

- `/new/request/`
- `/new/my-requests/`
- `/used/`
- `/used/category/<slug>/`
- `/used/<slug>/`
- `/accessories/`
- `/accessories/category/<slug>/`
- `/accessories/<slug>/`
- `/contact/`

### Cart & Orders

- `/cart/`
- `/cart/add/<app_label>/<pk>/`
- `/cart/remove/<item_id>/`
- `/cart/update/<item_id>/`
- `/cart/checkout/`
- `/cart/delivery-address/`
- `/cart/order-confirmation/<order_id>/`
- `/cart/cart-count/`

---

## 🛠️ Setup Guide

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the server:

```bash
python manage.py runserver
```

6. Visit:

`http://127.0.0.1:8000/`

7. Optional: configure SMTP and Twilio for real email/SMS delivery.

---

## 🎨 Design Notes

- Clean section layout with badge-style headings
- Table-based feature summary for clarity
- Emoji-enhanced content for quick scanning
- Landing-page structure for a polished README experience

---

## 💡 Notes

- `contact/README.md` includes contact app details
- `all_pages_links.txt` may contain SEO or sitemap page data

---

## ✅ Final Summary

A designer-friendly README for a Django e-commerce platform featuring product catalogs, account security, cart/checkout flow, support inquiries, and admin management.
