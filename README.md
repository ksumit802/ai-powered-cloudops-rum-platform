# AI-Powered CloudOps RUM & User Behavior Analytics Platform

An application monitoring and analytics platform that captures real user interactions, tracks user journeys, and provides operational visibility into cloud services.

The project combines **Real User Monitoring (RUM)** with cloud operations data to demonstrate how user experience and service health can be monitored from a unified dashboard.

> **Project status:** Work in Progress  
> **Environment:** Local demonstration environment using synthetic operational data and browser-generated test events.

## Project Overview

Traditional infrastructure monitoring focuses on server availability, CPU utilization, memory, and network performance. However, these metrics do not always reveal whether users can successfully complete their tasks.

This project explores how Real User Monitoring can help bridge that gap by capturing browser interactions and correlating user activity with operational information.

The platform aims to provide a unified view of:

- User activity and application interactions
- User journey and task completion tracking
- Cloud service availability and health
- Operational incidents
- Support ticket management
- User behavior analytics

## Key Features

### 1. Real User Monitoring (RUM)
- Browser-based event tracking using JavaScript.
- Captures page views and feature interactions.
- Tracks task initiation, completion, and failure.
- Records session identifiers and event timestamps.
- Sends collected events to a Flask backend.

### 2. Cloud Operations Dashboard
- Service availability overview.
- Active incident count.
- Support ticket count.
- Unique user sessions.
- Centralized operational dashboard.

### 3. Service Health Monitoring
- Displays cloud service information.
- Tracks service availability and response time.
- Identifies healthy, degraded, and maintenance states.

### 4. Incident Management
- Displays operational incidents.
- Includes severity and incident status.
- Provides visibility into service-related issues.

### 5. Support Ticket Management
- Users can submit support tickets through the dashboard.
- Tickets are stored in SQLite.
- Ticket creation is connected to RUM task tracking.

### 6. User Behavior Analytics
- Collects user interaction events.
- Analyses task completion and failure events.
- Uses Pandas for event processing and analytics.

## Architecture

```text
             User Browser
                  |
                  v
          Frontend Dashboard
           HTML / CSS / JS
                  |
                  v
          RUM Instrumentation
          (JavaScript Tracking)
                  |
                  v
             Flask Backend
                  |
          +-------+--------+
          |                |
          v                v
      SQLite DB       REST APIs
          |                |
          v                v
    RUM Events       Dashboard Data
    User Sessions    Services
    Support Tickets  Incidents
          |
          v
     Pandas Analytics
          |
          v
    User Behavior Insights
```

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | SQLite |
| Analytics | Pandas |
| Event Collection | JavaScript Fetch API |
| Version Control | Git, GitHub |

## Project Structure

```text
ai-powered-cloudops-rum-platform/
│
├── app.py
├── analytics.py
├── seed_demo_data.py
├── requirements.txt
├── README.md
│
├── data/
│   └── rum.db
│
├── templates/
│   └── index.html
│
├── static/
│   ├── dashboard.js
│   ├── rum.js
│   └── style.css
│
└── .gitignore
```

The local SQLite database is generated when the application runs and is intentionally excluded from version control.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- VS Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/ksumit802/ai-powered-cloudops-rum-platform.git
cd ai-powered-cloudops-rum-platform
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate demonstration data

```bash
python seed_demo_data.py
```

This generates synthetic services, incidents, tickets, and RUM events for demonstration purposes.

### 5. Start the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

## API Overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/events` | POST | Collect RUM events |
| `/api/events` | GET | Retrieve RUM events |
| `/api/tickets` | POST | Create support tickets |
| `/api/dashboard/summary` | GET | Retrieve dashboard KPIs |

## Analytics Approach

The analytics component uses Pandas to process collected RUM events.

Planned and ongoing analysis includes:

- User session analysis.
- Feature usage analysis.
- Task completion rate.
- Task failure analysis.
- Task duration analysis.
- User journey and abandonment analysis.

## Roadmap

- [x] Flask application and SQLite database.
- [x] Browser-based RUM event collection.
- [x] User session and feature interaction tracking.
- [x] Support ticket creation.
- [x] Synthetic demonstration data.
- [x] Initial CloudOps dashboard.
- [x] Basic Pandas analytics.
- [ ] Dynamic service health and incident views.
- [ ] Interactive user behavior visualizations.
- [ ] User journey and abandonment analysis.
- [ ] AI-powered operational insights.
- [ ] Correlation between user experience and service health.
- [ ] Docker containerization and deployment.

## Demonstration Data

This project currently uses synthetic operational data to demonstrate dashboard functionality.

Synthetic records are marked separately from manually generated browser testing events. Service availability and incident information are illustrative and should not be interpreted as live production monitoring data.

## Project Objective

The long-term objective is to explore how Real User Monitoring, behavioral analytics, and AI-assisted insights can support cloud operations teams in identifying user-facing issues and improving application reliability.

**Developed as a cloud operations and data analytics portfolio project.**