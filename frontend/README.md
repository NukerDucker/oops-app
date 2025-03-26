# OOPS App

OOPS App is a full-stack application for managing patients, treatments, and medical history. It consists of a **backend** built with Flask and a **frontend** built with React and Vite.

## Table of Contents
- [OOPS App](#oops-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
    - [Patients](#patients)
    - [Treatments](#treatments)
    - [History](#history)
  - [Troubleshooting](#troubleshooting)

## Features
- Patient management (add, update, delete, view)
- Treatment and prescription tracking
- Patient history management
- Role-based access control (Admin, Doctor, Receptionist)
- JWT-based authentication

## Prerequisites
Before running the application, ensure you have the following installed:
- **Python 3.8+**
- **Node.js 16+** and **npm** or **yarn**
- **Git**

## Setup Instructions

### Backend Setup
Navigate to the backend directory:  
```bash
cd backend
```
Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
Run the Flask development server:
```bash
flask run
```
---
### Frontend Setup
Navigate to the frontend directory:
```bash
cd frontend
```
Install the required dependencies:

```bash
npm install
# Or, if using yarn:
yarn install
```

Start the development server:
```
npm run dev
# Or, if using yarn:
yarn dev
```

## Running the Application
- Start the backend server by following the Backend Setup instructions.
- Start the frontend server by following the Frontend Setup instructions.
- Open your browser and navigate to http://127.0.0.1:5173 to access the application.

## API Endpoints
### Patients
`GET /api/patients` - Fetch all patients

`GET /api/patients/<int:patient_id>` - Fetch a specific patient

`POST /api/patients/add` - Add a new patient

`PUT /api/patients/update/<int:patient_id>` - Update patient details

`DELETE /api/patients/delete/<int:patient_id>` - Delete a patient

### Treatments
`POST /api/patients/<int:patient_id>`/treatments - Add a treatment

`GET /api/patients/<int:patient_id>/treatments` - Fetch treatments for a patient

`PUT /api/patients/<int:patient_id>/treatments/<int:treatment_id>` - Update a treatment

`DELETE /api/patients/<int:patient_id>/treatments/<int:treatment_id>` - Delete a treatment

### History
`POST /api/patients/<int:patient_id>/history/add` - Add a history entry

`GET /api/patients/<int:patient_id>/history` - Fetch patient history

`DELETE /api/patients/<int:patient_id>/history/delet`e - Delete a history entry

## Troubleshooting
- Backend not starting: Ensure all dependencies are installed and the virtual environment is activated.

- Frontend not starting: Ensure node_modules is installed by running npm install or yarn install.

- CORS issues: Ensure the backend has CORS enabled for the frontend's origin.

- Authentication errors: Ensure you are using a valid JWT token for API requests.