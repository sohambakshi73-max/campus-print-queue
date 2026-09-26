# Campus Print Queue & Pickup Tracker

A lightweight web application built with Python Flask and SQLite to manage and streamline printing queues across campus labs. Integrated with GitHub Actions CI/CD and hosted on Render.

## Features

- **Queue Management**: Submit print jobs with document title, student name, and page counts.
- **Status Tracking**: Transition jobs from `Queued` to `Ready for Pickup`.
- **Queue Maintenance**: Bulk clear completed pickup jobs.
- **REST API**: Expose active queue items via `/api/jobs` endpoint.
- **Health Check**: `/health` endpoint returning system availability and active deployment commit SHA.

---

## Local Setup & Execution

### Prerequisites
- Python 3.10+
- Virtual Environment (`venv`)

### Installation & Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/sohambakshi73-max/campus-print-queue.git](https://github.com/sohambakshi73-max/campus-print-queue.git)
   cd campus-print-queue