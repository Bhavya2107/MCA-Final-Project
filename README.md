<div align="center">

# 🖥️ COMPUTER & CCTV HUB

### A polished Django marketplace for laptops, accessories, support, and orders.

![Django](https://img.shields.io/badge/Django-6.0.4-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-1e3a5f?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-12.2.0-0d2244?style=for-the-badge)
![License](https://img.shields.io/badge/Status-Active-00d4ff?style=for-the-badge)

</div>

---

## 📌 Project Overview

**COMPUTER & CCTV HUB** is a designer-style Django e-commerce platform built to manage electronics, laptops, accessories, and customer service requests. It features a full shopping flow, secure user accounts, and a robust admin interface.

---

## 🧩 Core Applications

| App | Role |
|---|---|
| `accounts` | Registration, login, OTP verification, password recovery, and user profiles |
| `accessories` | Accessories catalog with categories, filters, product details, and inquiries |
| `used_laptops` | Used laptop listings, categories, detailed specs, and inquiries |
| `cart` | Cart management, checkout, delivery address, and order processing |
| `contact` | Contact page, inquiry handling, email notifications, and business info |
| `new_laptops` | Request a laptop workflow, request tracking, and notification emails |

---

## ✨ Experience Highlights

### 🔐 Secure User Journey

- Email + phone registration
- OTP verification before account activation
- Login with username or email
- Password reset links via email
- Profile view, edit, and password change

### 🛒 Modern Shopping Flow

- Product categories and dynamic filtering
- Product detail pages with inquiry capture
- Add items from multiple apps into one shared cart
- GST automatically calculated at **18%**
- Delivery pricing logic based on location
- Smooth checkout with order confirmation

### 📬 Contact & Support

- Contact page with configurable business information
- Inquiry submissions saved in the database
- Admin-friendly CSV export of inquiries
- Email notifications for support actions

### 💼 Laptop Request Workflow

- User request form for unavailable laptops
- Request tracking for customers and admins
- Notifications sent to users and owner
- Admin workflow for `pending` / `completed` / `rejected` statuses

---

## 📁 Project Structure

```
Website/
├── manage.py               # Django project entrypoint
├── db.sqlite3              # Default SQLite database
├── requirements.txt        # Dependency list
├── static/                 # CSS, JS, and image assets
├── media/                  # Uploaded images and files
├── templates/              # Shared HTML templates
├── Website/
│   ├── settings.py         # App configuration
│   └── urls.py             # Site-level routing
├── accounts/               # User auth & profiles
├── accessories/            # Accessories catalog
├── cart/                   # Cart & order processing
├── contact/                # Contact & inquiries
├── new_laptops/            # Laptop request workflow
└── used_laptops/           # Used laptop listings
```

---

## 📦 Dependencies

```
Django==6.0.4
pillow==12.2.0
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2026.1
```

> **Note:** Twilio is referenced in the code for SMS OTP but is not installed by default. If Twilio is absent, OTP codes are printed to the console for development.

---

## ⚙️ Configuration

### 🗄️ Database

- Default engine: **SQLite** (`db.sqlite3`)

### 📁 Static & Media

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 🌐 Localization

- Default language: `en-us`
- Supported languages: `English`, `Thai (ไทย)`
- Locale path: `BASE_DIR / 'locale'`

### 📧 Email

- Default backend: `console.EmailBackend` *(for development)*
- SMTP settings are available but commented out

Recommended environment variables:

```env
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
NEW_LAPTOP_REQUEST_NOTIFICATION_EMAIL=notify@email.com
```

### 📱 SMS OTP (Optional — Twilio)

```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 🔒 Security

- `DEBUG = True` for local development
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`
- Dev-friendly CSRF/session cookie settings
- Secure headers enabled for **XSS** and **MIME sniffing** protection

---

## 🌐 Site Pages & Routes

### Core Pages

| URL | Description |
|---|---|
| `/` | Home |
| `/about/` | About page |
| `/privacy/` | Privacy policy |
| `/terms/` | Terms of service |
| `/developer/` | Developer info |

### Account Pages

| URL | Description |
|---|---|
| `/accounts/register/` | User registration |
| `/accounts/verify-otp/<user_id>/` | OTP verification |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/forgot-password/` | Forgot password |
| `/accounts/reset-password/<token>/` | Password reset |
| `/accounts/profile/` | View profile |
| `/accounts/profile/edit/` | Edit profile |
| `/accounts/change-password/` | Change password |

### Product Pages

| URL | Description |
|---|---|
| `/new/request/` | Request a new laptop |
| `/new/my-requests/` | View my requests |
| `/used/` | Used laptop listing |
| `/used/category/<slug>/` | Filter by category |
| `/used/<slug>/` | Laptop detail |
| `/accessories/` | Accessories listing |
| `/accessories/category/<slug>/` | Filter by category |
| `/accessories/<slug>/` | Accessory detail |
| `/contact/` | Contact page |

### Cart & Orders

| URL | Description |
|---|---|
| `/cart/` | View cart |
| `/cart/add/<app_label>/<pk>/` | Add item to cart |
| `/cart/remove/<item_id>/` | Remove item |
| `/cart/update/<item_id>/` | Update quantity |
| `/cart/checkout/` | Checkout |
| `/cart/delivery-address/` | Set delivery address |
| `/cart/order-confirmation/<order_id>/` | Order confirmation |
| `/cart/cart-count/` | Live cart count (AJAX) |

---

## 🛠️ Setup Guide

**1. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Apply database migrations**

```bash
python manage.py migrate
```

**4. Create a superuser**

```bash
python manage.py createsuperuser
```

**5. Run the development server**

```bash
python manage.py runserver
```

**6. Open in your browser**

```
http://127.0.0.1:8000/
```

**7. *(Optional)* Configure SMTP and Twilio**

Set the environment variables listed in the Configuration section above for real email and SMS OTP delivery.

---

## 💡 Notes

- `contact/README.md` includes additional contact app details
- `all_pages_links.txt` may contain SEO or sitemap page data

---

## ✅ Final Summary

A designer-friendly Django e-commerce platform featuring:

- ✅ Product catalogs — used laptops, new laptop requests, accessories
- ✅ Secure account system — OTP, email login, password reset
- ✅ Full cart & checkout — GST, delivery pricing, order confirmation
- ✅ Support inquiries — contact forms, CSV export, admin notifications
- ✅ Admin management — status workflows, request tracking, email alerts

---

<div align="center">

### 🔄 Updates In Progress

> **New features and improvements are currently being developed.**
> Stay tuned — changes will be released in upcoming versions.

![In Progress](https://img.shields.io/badge/Development-In%20Progress-00d4ff?style=for-the-badge&logo=github&logoColor=white)

</div>
