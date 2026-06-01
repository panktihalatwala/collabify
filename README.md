# 🚀 Collabify — Influencer Marketing Platform

<div align="center">

![Collabify](https://img.shields.io/badge/Collabify-Connect%20%7C%20Collaborate%20%7C%20Grow-7c3aed?style=for-the-badge&logo=django&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**The #1 Influencer Marketing Platform for India**

*Connecting brands and creators for powerful, authentic collaborations*

</div>

---

## 📌 What is Collabify?

**Collabify** is a full-stack, production-ready **Influencer Marketing Platform** built with Django. It bridges the gap between **Indian brands** and **content creators**, providing a seamless end-to-end workflow — from discovery to collaboration to payment tracking.

> Think **Upwork meets Instagram meets LinkedIn** — built for the Indian creator economy.

---

## ✨ Features

### 👤 For Creators
- Beautiful creator profile with portfolio showcase
- Social media stats — followers, engagement rate, niche
- Set collaboration pricing in ₹
- Browse and apply to brand campaigns
- Accept / Reject / Counter collaboration requests
- Real-time chat with brands
- Instant notifications for every activity
- Receive verified reviews and ratings
- Earnings and collaboration dashboard

### 🏢 For Brands
- Professional company profile with verified badge
- Create and manage campaigns with full control
- Discover creators by niche, followers, engagement
- Bookmark favourite creators
- Real-time messaging with creators
- Campaign analytics with Chart.js
- Send direct collaboration requests
- Rate and review creators post-collaboration

### 🛡️ For Admins
- Full Django Admin panel
- User management and suspension
- Campaign approval system
- Report and complaint resolution

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.14, Django 6.0 |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **Database** | SQLite (dev) → PostgreSQL (prod) |
| **Real-time** | Django Channels, WebSockets |
| **Charts** | Chart.js |
| **Auth** | Django Authentication, Role-based permissions |
| **Architecture** | MVT Pattern, Django ORM |
| **Storage** | WhiteNoise, Pillow |

---

## 📁 Project Structure

```
collabify_project/
│
├── collabify/                  # Main Django project settings
├── accounts/                   # Authentication & users
├── influencers/                # Creator management
├── brands/                     # Brand management
├── campaigns/                  # Campaign system
├── messaging/                  # Real-time chat
├── notifications/              # Notification system
├── reviews/                    # Ratings & reviews
├── reports/                    # User reporting
├── dashboard/                  # Analytics dashboards
├── templates/                  # All HTML templates
├── static/                     # Static assets
├── media/                      # User uploaded files (gitignored)
├── manage.py                   # Django management commands
├── seed.py                     # Demo data seeder
└── .gitignore
```