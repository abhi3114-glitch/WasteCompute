# WasteCompute

**Microsoft Imagine Cup 2026 Submission**

WasteCompute is a distributed compute marketplace that enables enterprises to monetize unused CPU and GPU capacity while helping buyers access affordable compute resources. The platform addresses the global problem of idle infrastructure waste, aligning with UN Sustainable Development Goals 9, 12, and 13.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [Usage](#usage)
8. [API Reference](#api-reference)
9. [Architecture](#architecture)
10. [Sustainability Impact](#sustainability-impact)
11. [Business Model](#business-model)
12. [Roadmap](#roadmap)
13. [Team](#team)
14. [License](#license)

---

## Problem Statement

Over $30 billion worth of compute resources sit idle in enterprise data centers every year. Companies overprovision infrastructure to handle peak loads, but during off-peak hours, this capacity goes unused. This results in:

- Wasted energy consumption
- Unnecessary hardware purchases
- Increased carbon emissions
- Higher operational costs

Meanwhile, AI startups, researchers, and developers struggle to afford compute time for training models, running simulations, and processing data.

---

## Solution Overview

WasteCompute creates a secure marketplace connecting enterprises with idle compute capacity to buyers who need affordable resources.

### How It Works

```
Enterprise (Seller)          WasteCompute Platform          Buyer
     |                              |                         |
     |-- Register idle nodes ------>|                         |
     |                              |<-- Submit workload -----|
     |<-- Execute securely ---------|                         |
     |-- Return results ----------->|                         |
     |                              |-- Deliver output ------>|
     |<-- Receive payment ----------|                         |
```

Key benefits:
- Enterprises monetize unused infrastructure
- Buyers access compute at reduced rates
- Environment benefits from optimized resource utilization

---

## Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| Job Execution | Submit CPU or GPU workloads via dashboard or API |
| Node Provisioning | Auto-detect hardware specifications (CPU, RAM, GPU) |
| Resource Selection | Choose between CPU and GPU for job execution |
| Live Terminal | Real-time console output during job execution |
| Job History | Persistent audit log of all executed jobs |

### Infrastructure

| Feature | Description |
|---------|-------------|
| SQLite Persistence | Jobs and nodes survive server restarts |
| Hardware Detection | Automatic detection of CPU percentage, RAM, and GPU model |
| Sandboxed Execution | Isolated subprocess execution for security |
| Resource Monitoring | Real-time tracking of CPU and memory usage |

### Analytics and Billing

| Feature | Description |
|---------|-------------|
| Usage Tracking | Track compute time per job and per resource type |
| Dynamic Pricing | Peak and off-peak pricing multipliers |
| Carbon Tracking | Calculate CO2 savings from compute reuse |
| Invoice Generation | Automatic billing based on usage |

### User Interface

| Feature | Description |
|---------|-------------|
| 3D Landing Page | Three.js visualization with CPU and GPU models |
| Enterprise Dashboard | Professional dark-mode console interface |
| Responsive Design | Works on desktop and tablet devices |

---

## Technology Stack

### Backend
- Python 3.9+
- FastAPI (REST API framework)
- SQLite (persistent storage)
- Pydantic (data validation)
- psutil (hardware detection)

### Frontend
- HTML5, CSS3, JavaScript
- Three.js (3D visualization)
- Inter and JetBrains Mono fonts

### Deployment
- Docker
- uvicorn (ASGI server)

---

## Project Structure

```
WasteCompute/
├── backend/
│   ├── api/                 # FastAPI route handlers
│   │   ├── jobs.py          # Job submission and history
│   │   ├── nodes.py         # Node provisioning and listing
│   │   ├── billing.py       # Invoice generation
│   │   ├── analytics.py     # Usage and sustainability stats
│   │   └── metrics.py       # System metrics
│   ├── database/
│   │   ├── db.py            # SQLite database operations
│   │   └── models.py        # Pydantic data models
│   ├── executor/
│   │   ├── sandbox.py       # Sandboxed job execution
│   │   ├── monitor.py       # Process monitoring
│   │   └── limits.py        # Resource limit enforcement
│   ├── scheduler/
│   │   ├── scheduler.py     # Job scheduling logic
│   │   └── scoring.py       # Node selection algorithm
│   └── app.py               # FastAPI application entry point
├── frontend/
│   ├── css/
│   │   └── styles.css       # Enterprise dark theme
│   ├── js/
│   │   ├── api.js           # API helper functions
│   │   ├── dashboard.js     # Dashboard logic
│   │   ├── jobs.js          # Job submission handling
│   │   ├── nodes.js         # Node display logic
│   │   ├── hero_3d.js       # Three.js 3D scene
│   │   └── animations.js    # Motion animations
│   ├── index.html           # Landing page
│   ├── dashboard.html       # Admin console
│   └── docs.html            # Product documentation
├── analytics/
│   ├── usage_tracker.py     # Usage data collection
│   └── sustainability.py    # Carbon footprint calculations
├── billing/
│   ├── calculator.py        # Cost calculation
│   ├── pricing.py           # Dynamic pricing model
│   └── invoices.py          # Invoice generation
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── DEMO_SCRIPT.md           # Presentation guide
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/abhi3114-glitch/WasteCompute.git
cd WasteCompute
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python -m uvicorn backend.app:app --reload --port 8001
```

4. Open in browser:
```
http://localhost:8001/app/index.html
```

---

## Usage

### Landing Page

Navigate to `/app/index.html` to view the product landing page with 3D visualization.

### Dashboard

Navigate to `/app/dashboard.html` to access the admin console.

#### Console View
- Enter a command in the input field
- Select CPU or GPU from the dropdown
- Click Execute to run the job
- View output in the live terminal
- Check job history in the table below

#### Nodes View
- Click "Provision Node" to add a compute node
- View detected hardware specifications
- Monitor node status (idle/busy)

#### Invoices View
- View billing summary
- Check transaction history
- See usage-based costs

---

## API Reference

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jobs/submit/` | Submit a job for execution |
| GET | `/jobs/history/` | Get list of all executed jobs |

#### Submit Job Request Body
```json
{
  "command": "python script.py",
  "max_runtime": 60,
  "resource_type": "cpu"
}
```

### Nodes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/nodes/provision` | Provision a new compute node |
| GET | `/nodes/` | List all registered nodes |
| POST | `/nodes/heartbeat` | Update node status |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/usage` | Get usage records |
| GET | `/analytics/sustainability` | Get carbon savings metrics |
| GET | `/analytics/summary` | Get aggregated stats |

### Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/invoice` | Get detailed invoice |
| GET | `/billing/pricing` | Get current pricing rates |
| GET | `/billing/summary` | Get billing summary |

---

## Architecture

### System Flow

```
User Request
     |
     v
[FastAPI Router] --> [Scheduler] --> [Executor]
     |                    |              |
     v                    v              v
[Database]         [Scoring]      [Monitor]
     |                    |              |
     v                    v              v
[SQLite]           [Node Selection]  [Resource Limits]
```

### Data Flow

1. User submits job via dashboard or API
2. Scheduler selects best available node
3. Executor runs job in sandboxed subprocess
4. Monitor tracks resource usage
5. Results stored in SQLite database
6. Usage tracker records metrics
7. Billing calculates costs

---

## Sustainability Impact

WasteCompute contributes to environmental sustainability by:

### UN Sustainable Development Goals

| Goal | Contribution |
|------|-------------|
| SDG 9: Industry and Innovation | Democratizes access to compute infrastructure |
| SDG 12: Responsible Consumption | Extends hardware lifecycle, reduces waste |
| SDG 13: Climate Action | Optimizes energy use, reduces carbon footprint |

### Carbon Savings Calculation

The platform tracks carbon savings based on:
- Compute time reused (avoiding new hardware procurement)
- Energy efficiency of shared resources
- Reduced idle power consumption

Metrics displayed in dashboard:
- CO2 saved (kg)
- Tree equivalents
- Sustainability score

---

## Business Model

### Revenue Streams

1. Transaction Fee: 15% of compute revenue
2. Enterprise Tier: Enhanced security and SLA guarantees
3. Research Discount: Subsidized rates for academic institutions

### Pricing Model

| Resource | Base Rate | Peak Multiplier | Off-Peak Multiplier |
|----------|-----------|-----------------|---------------------|
| CPU | $0.001/sec | 1.5x | 0.8x |
| GPU | $0.005/sec | 1.5x | 0.8x |

Peak hours: 9:00-11:00, 14:00-16:00 (local time)

---

## Roadmap

### Completed

- [x] MVP with CPU/GPU scheduling
- [x] Real hardware detection
- [x] SQLite persistence
- [x] Enterprise dashboard UI
- [x] Sustainability tracking
- [x] Dynamic pricing

### Planned

- [ ] Azure cloud deployment
- [ ] Multi-tenant isolation
- [ ] GPU partitioning (NVIDIA MIG)
- [ ] Kubernetes orchestration
- [ ] Mobile application
- [ ] Blockchain-based payments

---

---

## License

MIT License

Copyright (c) 2026 WasteCompute Team

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**Built for Microsoft Imagine Cup 2026**
