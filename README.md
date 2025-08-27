# Automated Refund Dashboard System for SabPaisa

## Overview
This project provides a web-based dashboard for SabPaisa operations teams to automate refund reconciliation and processing. It features:
- Transaction search by ID and filters
- Excel upload and parsing
- Auto-validation of refund data
- Refund trigger (JSON/API)
- Audit log
- Visualization panel (charts, metrics)

## Tech Stack
- **Backend:** Python (FastAPI), pandas
- **Frontend:** HTML/JavaScript (can be extended to React)

## Getting Started
1. Install Python 3.9+
2. Install dependencies:
   ```
   pip install fastapi uvicorn pandas openpyxl
   ```
3. Run the backend:
   ```
   uvicorn backend.main:app --reload
   ```
4. Open `frontend/index.html` in your browser for the dashboard UI.

## Folder Structure
- `backend/` – FastAPI backend, Excel parsing, validation, API endpoints
- `frontend/` – HTML/JS dashboard UI
- `.github/` – Copilot instructions
- `.vscode/` – VS Code tasks/config

## Next Steps
- Implement backend endpoints for upload, search, validation, refund trigger, and audit log
- Build frontend for file upload, search, and dashboard
- Add charts and metrics

---
For questions or contributions, contact the project maintainer.
