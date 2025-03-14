from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from modules.user import User
from modules.task import Task
from modules.patient import Patient
from modules.supply import Supply
from modules.medication import Medication
from modules.appointment import Appointment
from modules.fee import Fee
from modules.lab_result import LabResult
from modules.prescription import Prescription
from modules.treatment import Treatment
from modules.system import System
from datetime import date, time, datetime, timedelta

# Import route blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.patients import patients_bp
from routes.inventory import inventory_bp
from routes.appointments import appointments_bp
from routes.medications import medications_bp
from routes.financials import financials_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this in production

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Create a function to initialize mock data
def initialize_mock_data():
    # Initialize global variables
    global users, patients, supplies, appointments
    users = []
    patients = []
    supplies = []
    appointments = []
    
    # Initialize users
    initialize_users()
    # Initialize patients
    initialize_patients()
    # Initialize supplies
    initialize_supplies()
    # Initialize appointments
    initialize_appointments()

def initialize_users():
    """Create mock user accounts"""
    global users
    
    # Create hashed password once
    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
    
    # Admin user
    admin_user = User(1, "Admin", hashed_password, "admin")
    admin_user.add_access_permission("Inventory", "/inventory")
    admin_user.add_access_permission("Patient", "/patient")
    admin_user.add_access_permission("Main", "/main")
    
    # Admin tasks
    admin_user.add_task(Task(1, "Task 1", "This is task 1"))
    admin_user.add_task(Task(2, "Task 2", "This is task 2"))
    admin_user.add_task(Task(3, "Task 3", "This is task 3"))
    admin_user.add_weekly_task(Task(1, "Weekly Task 1", "This is weekly task 1"))
    admin_user.add_weekly_task(Task(2, "Weekly Task 2", "This is weekly task 2"))
    admin_user.add_emergency_task(Task(1, "Emergency Task 1", "This is emergency task 1"))
    users.append(admin_user)
    
    # Doctor users
    doctor1_user = User(2, "Doctor1", hashed_password, "doctor")
    doctor1_user.add_access_permission("Patient", "/patient")
    doctor1_user.add_access_permission("Main", "/main")
    doctor1_user.add_task(Task(1, "Follow-Up", "Mr. Napaul HIV checkup"))
    doctor1_user.add_task(Task(2, "Prescribe", "Mr. Bento paracetamol prescription"))
    doctor1_user.add_task(Task(3, "Patient Consultation", "Ms. Pepperoni experiencing heartburn"))
    doctor1_user.add_task(Task(4, "Physical Exam", "Routine checkup for Mr. Treadmill"))
    doctor1_user.add_weekly_task(Task(1, "Seminar @BKK", "Trans people seminar"))
    doctor1_user.add_weekly_task(Task(2, "Staff Meeting", "Discuss new hospital protocols"))
    doctor1_user.add_emergency_task(Task(1, "Code Blue", "Emergency resuscitation for Mr. Lightning"))
    users.append(doctor1_user)
    
    doctor2_user = User(3, "Doctor2", hashed_password, "doctor")
    doctor2_user.add_access_permission("Patient", "/patient")
    doctor2_user.add_access_permission("Main", "/main")
    doctor2_user.add_task(Task(1, "Follow-Up", "Mr. Sandwich toothache checkup"))
    doctor2_user.add_task(Task(2, "Annual Physical", "Routine checkup for Mr. Nuker Ducker"))
    doctor2_user.add_task(Task(3, "Diet Consultation", "Help Mr. Eat Bento with high cholesterol"))
    doctor2_user.add_task(Task(4, "Vision Test", "Check Ms. Polly Graph's eyesight"))
    doctor2_user.add_task(Task(5, "Blood Work Review", "Discuss test results with Mr. Nhow Socool"))
    doctor2_user.add_task(Task(6, "Allergy Test", "Determine cause of rash for Ms. Anna Conda"))
    doctor2_user.add_emergency_task(Task(1, "Euthanization", "Smoke you know who"))
    doctor2_user.add_emergency_task(Task(2, "Severe Allergic Reaction", "Ms. Karen Outage in anaphylactic shock"))
    doctor2_user.add_emergency_task(Task(3, "Cardiac Arrest", "Mr. Sir Render experiencing heart failure"))
    doctor2_user.add_weekly_task(Task(1, "Department Meeting", "Review monthly performance and improvements"))
    users.append(doctor2_user)
    
    # Receptionist users
    receptionist1_user = User(4, "Sally Smith", hashed_password, "Receptionist")
    receptionist2_user = User(5, "Megan Bright", hashed_password, "Receptionist")
    receptionist3_user = User(6, "Tina Turner", hashed_password, "Receptionist")
    users.append(receptionist1_user)
    users.append(receptionist2_user)
    users.append(receptionist3_user)

def initialize_patients():
    """Create mock patients with their records"""
    global patients
    
    # First set of patients (more detailed)
    patient1 = Patient("John Doe", 45, "Male", "555-1234")
    patient1.add_history_entry("Initial visit for chronic back pain - 2023-01-15")
    patient1.add_history_entry("Prescribed Naproxen for pain management - 2023-01-15")
    patient1.add_history_entry("Follow-up: Pain reduced by 30% - 2023-02-10")
    patients.append(patient1)
    
    patient2 = Patient("Jane Smith", 32, "Female", "555-5678")
    patient2.add_history_entry("Prenatal checkup, 24 weeks - 2023-03-05")
    patient2.add_history_entry("Ultrasound shows healthy development - 2023-03-05")
    patient2.add_history_entry("Follow-up: Blood pressure slightly elevated - 2023-04-02")
    patients.append(patient2)
    
    # Additional patients
    patient3 = Patient("Robert Johnson", 67, "Male", "555-9012")
    patient3.add_history_entry("Diagnosed with Type 2 Diabetes - 2022-11-12")
    patient3.add_history_entry("Started on Metformin - 2022-11-12")
    patient3.add_history_entry("Follow-up: Blood sugar levels improving - 2023-01-20")
    patient3.add_history_entry("Annual checkup: Kidney function normal - 2023-05-15")
    patients.append(patient3)
    
    patient4 = Patient("Emily Davis", 28, "Female", "555-3456")
    patient4.add_history_entry("Treatment for anxiety - 2023-02-18")
    patient4.add_history_entry("Prescribed Sertraline 50mg daily - 2023-02-18")
    patients.append(patient4)
    
    patient5 = Patient("Michael Wilson", 52, "Male", "555-7890")
    patient5.add_history_entry("Hypertension diagnosis - 2022-09-30")
    patient5.add_history_entry("Prescribed Lisinopril - 2022-09-30")
    patient5.add_history_entry("Cholesterol panel: LDL slightly elevated - 2023-04-25")
    patients.append(patient5)
    
    # Add more patients with creative names
    patient6 = Patient("Anna Conda", 22, "Female", "Snake@hiss.com")
    patient6.add_history_entry("2022-03-15: Treated for dehydration and muscle stiffness")
    patient6.add_treatment(Treatment("Fever and sore throat", "Strep throat", 
                    "Prescribed amoxicillin and advised rest", date(2025, 3, 3), True))
    patients.append(patient6)
    
    patient7 = Patient("Karen Outage", 45, "Female", "Manager@now.com")
    patient7.add_history_entry("2022-09-04: Treated for stress-related hypertension") 
    patient7.add_treatment(Treatment("Chest pain", "Costochondritis", 
                    "Prescribed ibuprofen and advised stretching exercises", 
                    date(2025, 1, 10), True))
    patients.append(patient7)

def initialize_supplies():
    """Create mock medical supplies inventory"""
    global supplies
    
    supplies.append(Supply("Paracetamol (Box of 100 tablets)", 50, 8.99, "Pain Relief"))
    supplies.append(Supply("Amoxicillin (Box of 50 capsules)", 30, 12.50, "Antibiotic"))
    supplies.append(Supply("Insulin Vials (10ml each)", 45, 5.25, "Diabetes Management"))
    supplies.append(Supply("Blood Pressure Medication (Bottle of 30 tablets)", 15, 45.99, "Cardiovascular"))
    supplies.append(Supply("Antihistamine (Box of 25 tablets)", 25, 18.75, "Allergy Relief"))
    supplies.append(Supply("Cough Syrup (Bottle of 250ml)", 20, 22.50, "Cold & Flu"))
    supplies.append(Supply("Ibuprofen (Box of 50 tablets)", 35, 7.99, "Pain Relief"))
    supplies.append(Supply("Antacid Chewables (Pack of 200)", 28, 15.50, "Digestive Health"))
    supplies.append(Supply("Epinephrine Auto-Injector", 40, 9.25, "Emergency Allergy Treatment"))
    supplies.append(Supply("Sleeping Pills (Box of 30 tablets)", 60, 6.50, "Sleep Aid"))

def initialize_appointments():
    """Create mock appointments"""
    global appointments, patients, users
    
    doctor1_id = 2  # Doctor1's ID
    doctor2_id = 3  # Doctor2's ID
    
    # Create appointments for the next 14 days
    for i in range(1, 15):
        appt_date = date.today() + timedelta(days=i)
        
        # Morning appointments
        if i % 3 != 0:  # Skip every third day for variety
            appointments.append(Appointment(
                patients[i % 5].id,
                doctor1_id,
                appt_date,
                time(9, 0)
            ))
            
            appointments.append(Appointment(
                patients[(i + 2) % 5].id,
                doctor2_id,
                appt_date,
                time(10, 30)
            ))
        
        # Afternoon appointments
        if i % 2 == 0:  # Every other day
            appointments.append(Appointment(
                patients[(i + 1) % 5].id,
                doctor1_id if i % 2 == 0 else doctor2_id,
                appt_date,
                time(14, 0)
            ))
    
    # Set some appointments to different statuses
    if appointments:
        appointments[0].update_status("completed")
        if len(appointments) > 1:
            appointments[1].update_status("cancelled")
        if len(appointments) > 3:
            appointments[3].update_status("no-show")

# Helper function used by multiple routes
def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

# Initialize mock data
initialize_mock_data()

# Create a System instance for receptionist functionality
system = System()

# Add existing patients to the system
for patient in patients:
    system.add_patient(patient)

# Share data with blueprints
import routes.auth
import routes.users
import routes.patients
import routes.inventory
import routes.appointments
import routes.medications
import routes.financials

# Share variables with blueprints
routes.auth.users = users
routes.auth.bcrypt = bcrypt
routes.users.users = users
routes.patients.users = users
routes.patients.patients = patients
routes.inventory.users = users
routes.inventory.supplies = supplies
routes.appointments.users = users
routes.appointments.patients = patients
routes.appointments.appointments = appointments
routes.medications.users = users
routes.medications.patients = patients
routes.financials.users = users
routes.financials.patients = patients
routes.financials.system = system

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(medications_bp)
app.register_blueprint(financials_bp)

if __name__ == '__main__':
    app.run(debug=True)
