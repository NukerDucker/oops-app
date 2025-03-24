from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import date, time, datetime, timedelta
import os
from dotenv import load_dotenv

# Import domain modules
from modules.system import System
from modules.user import User
from modules.task import Task
from modules.patient import Patient
from modules.supply import Supply
from modules.appointment import Appointment
from modules.treatment import Treatment
from modules.base_entity import BaseEntity

# Load environment variables
load_dotenv()

def create_app(config=None):
    """Application factory pattern to create the Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key_change_in_production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Important: Configure CORS properly to handle preflight OPTIONS requests
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize extensions
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    # Reset the ID counter for clean initialization
    BaseEntity.current_id = 0
    
    # Initialize system controller
    system = initialize_system(bcrypt)
    
    # Register blueprints with dependency injection
    register_blueprints(app, system, bcrypt)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def initialize_system(bcrypt):
    """Initialize the system with mock data"""
    system = System()
    
    # Create mock data
    initialize_users(system, bcrypt)
    initialize_patients(system)
    initialize_supplies(system)
    initialize_appointments(system)
    
    return system

def initialize_users(system, bcrypt):
    """Create mock user accounts in the system"""
    # Create hashed password once
    mock_password = os.environ.get('MOCK_PASSWORD', 'password')
    hashed_password = bcrypt.generate_password_hash(mock_password).decode('utf-8')
    
    # Admin user - let BaseEntity handle ID generation
    admin_user = User(username="Admin", password_hash=hashed_password, user_type="admin")
    admin_user.add_access_permission("Inventory", "/inventory")
    admin_user.add_access_permission("Patient", "/patient")
    admin_user.add_access_permission("Appointments", "/appointments")
    admin_user.add_access_permission("Main", "/main")
    
    # Admin tasks - let BaseEntity handle ID generation
    admin_user.add_task(Task(title="Review Patient Reports", description="Review weekly patient outcome reports"))
    admin_user.add_task(Task(title="Staff Performance Review", description="Complete quarterly staff evaluations"))
    admin_user.add_task(Task(title="Budget Planning", description="Finalize next quarter budget allocations"))
    admin_user.add_weekly_task(Task(title="Executive Meeting", description="Hospital board strategic planning"))
    admin_user.add_weekly_task(Task(title="Department Heads Meeting", description="Coordination meeting with all departments"))
    admin_user.add_emergency_task(Task(title="Emergency Response Planning", description="Update emergency protocols"))
    system.add_user(admin_user)
    
    # Doctor users
    doctor1_user = User(username="Dr. Sarah Chen", password_hash=hashed_password, user_type="doctor")
    doctor1_user.add_access_permission("Patient", "/patient")
    doctor1_user.add_access_permission("Main", "/main")
    doctor1_user.add_task(Task(title="Follow-Up Appointment", description="Follow up with Mr. Thompson about recovery"))
    doctor1_user.add_task(Task(title="Medication Review", description="Review Mr. Jackson's prescription regimen"))
    doctor1_user.add_task(Task(title="Patient Consultation", description="Initial consultation with Ms. Rodriguez"))
    doctor1_user.add_task(Task(title="Physical Examination", description="Annual physical for Mr. Williams"))
    doctor1_user.add_weekly_task(Task(title="Medical Conference", description="Attend cardiology advances seminar"))
    doctor1_user.add_weekly_task(Task(title="Staff Meeting", description="Discuss new hospital protocols"))
    doctor1_user.add_emergency_task(Task(title="Code Blue Response", description="Emergency resuscitation protocol review"))
    system.add_user(doctor1_user)
    
    doctor2_user = User(username="Dr. James Wilson", password_hash=hashed_password, user_type="doctor")
    doctor2_user.add_access_permission("Patient", "/patient")
    doctor2_user.add_access_permission("Main", "/main")
    doctor2_user.add_task(Task(title="Follow-Up Appointment", description="Check Mr. Sanders' recovery from dental procedure"))
    doctor2_user.add_task(Task(title="Annual Physical", description="Routine checkup for Mr. Peterson"))
    doctor2_user.add_task(Task(title="Diet Consultation", description="Discuss nutrition plan with Mr. Garcia"))
    doctor2_user.add_task(Task(title="Vision Assessment", description="Evaluate Ms. Johnson's vision changes"))
    doctor2_user.add_task(Task(title="Lab Results Review", description="Review and explain blood work to Mr. Mitchell"))
    doctor2_user.add_task(Task(title="Allergy Testing", description="Conduct allergy panel for Ms. Anna Coleman"))
    doctor2_user.add_emergency_task(Task(title="Critical Care Consultation", description="Evaluate ICU patient condition"))
    doctor2_user.add_emergency_task(Task(title="Allergic Reaction Protocol", description="Review severe allergic reaction treatment"))
    doctor2_user.add_emergency_task(Task(title="Cardiac Emergency Response", description="Update cardiac arrest response procedures"))
    doctor2_user.add_weekly_task(Task(title="Department Meeting", description="Review monthly performance metrics"))
    system.add_user(doctor2_user)
    
    # Receptionist users
    receptionist1_user = User(username="Sally Smith", password_hash=hashed_password, user_type="receptionist")
    receptionist2_user = User(username="Megan Bright", password_hash=hashed_password, user_type="receptionist")
    receptionist3_user = User(username="Tina Turner", password_hash=hashed_password, user_type="receptionist")
    system.add_user(receptionist1_user)
    system.add_user(receptionist2_user)
    system.add_user(receptionist3_user)

def initialize_patients(system):
    """Create mock patients with their records"""
    # First set of patients (more detailed)
    patient1 = Patient(name="John Doe", age=45, gender="Male", contact="555-1234")
    patient1.add_history_entry("Initial visit for chronic back pain - 2023-01-15")
    patient1.add_history_entry("Prescribed Naproxen for pain management - 2023-01-15")
    patient1.add_history_entry("Follow-up: Pain reduced by 30% - 2023-02-10")
    system.add_patient(patient1)
    
    patient2 = Patient(name="Jane Smith", age=32, gender="Female", contact="555-5678")
    patient2.add_history_entry("Prenatal checkup, 24 weeks - 2023-03-05")
    patient2.add_history_entry("Ultrasound shows healthy development - 2023-03-05")
    patient2.add_history_entry("Follow-up: Blood pressure slightly elevated - 2023-04-02")
    system.add_patient(patient2)
    
    # Additional patients
    patient3 = Patient(name="Robert Johnson", age=67, gender="Male", contact="555-9012")
    patient3.add_history_entry("Diagnosed with Type 2 Diabetes - 2022-11-12")
    patient3.add_history_entry("Started on Metformin - 2022-11-12")
    patient3.add_history_entry("Follow-up: Blood sugar levels improving - 2023-01-20")
    patient3.add_history_entry("Annual checkup: Kidney function normal - 2023-05-15")
    system.add_patient(patient3)
    
    patient4 = Patient(name="Emily Davis", age=28, gender="Female", contact="555-3456")
    patient4.add_history_entry("Treatment for anxiety - 2023-02-18")
    patient4.add_history_entry("Prescribed Sertraline 50mg daily - 2023-02-18")
    system.add_patient(patient4)
    
    patient5 = Patient(name="Michael Wilson", age=52, gender="Male", contact="555-7890")
    patient5.add_history_entry("Hypertension diagnosis - 2022-09-30")
    patient5.add_history_entry("Prescribed Lisinopril - 2022-09-30")
    patient5.add_history_entry("Cholesterol panel: LDL slightly elevated - 2023-04-25")
    system.add_patient(patient5)
    
    # Additional patients with more professional names and histories
    patient6 = Patient(name="Anna Coleman", age=22, gender="Female", contact="acoleman@email.com")
    patient6.add_history_entry("2022-03-15: Treated for dehydration and muscle fatigue")
    patient6.add_treatment(Treatment(
        symptoms="Fever and sore throat", 
        diagnosis="Strep throat",
        treatment="Prescribed amoxicillin and advised rest", 
        treatment_date=date(2023, 3, 3), 
        finished=True
    ))
    system.add_patient(patient6)
    
    patient7 = Patient(name="Karen Mitchell", age=45, gender="Female", contact="kmitchell@email.com")
    patient7.add_history_entry("2022-09-04: Treated for stress-related hypertension") 
    patient7.add_treatment(Treatment(
        symptoms="Chest pain", 
        diagnosis="Costochondritis",
        treatment="Prescribed ibuprofen and advised stretching exercises", 
        treatment_date=date(2023, 1, 10), 
        finished=True
    ))
    system.add_patient(patient7)

def initialize_supplies(system):
    """Create mock medical supplies inventory"""
    supplies = [
        Supply(name="Paracetamol (Box of 100 tablets)", quantity=50, unit_price=8.99, category="Pain Relief"),
        Supply(name="Amoxicillin (Box of 50 capsules)", quantity=30, unit_price=12.50, category="Antibiotic"),
        Supply(name="Insulin Vials (10ml each)", quantity=45, unit_price=5.25, category="Diabetes Management"),
        Supply(name="Blood Pressure Medication (Bottle of 30 tablets)", quantity=15, unit_price=45.99, category="Cardiovascular"),
        Supply(name="Antihistamine (Box of 25 tablets)", quantity=25, unit_price=18.75, category="Allergy Relief"),
        Supply(name="Cough Syrup (Bottle of 250ml)", quantity=20, unit_price=22.50, category="Cold & Flu"),
        Supply(name="Ibuprofen (Box of 50 tablets)", quantity=35, unit_price=7.99, category="Pain Relief"),
        Supply(name="Antacid Chewables (Pack of 200)", quantity=28, unit_price=15.50, category="Digestive Health"),
        Supply(name="Epinephrine Auto-Injector", quantity=40, unit_price=9.25, category="Emergency Allergy Treatment"),
        Supply(name="Sleeping Pills (Box of 30 tablets)", quantity=60, unit_price=6.50, category="Sleep Aid")
    ]
    
    for supply in supplies:
        system.add_supply(supply)

def initialize_appointments(system):
    """Create mock appointments"""
    # Get users with doctor role - no hardcoded IDs
    doctors = [user for user in system._users.values() if user.user_type == "doctor"]
    if len(doctors) < 2:
        print("Warning: Not enough doctors for appointment initialization")
        return
    
    doctor1_id = doctors[0].id  # First doctor's ID
    doctor2_id = doctors[1].id  # Second doctor's ID
    
    # Get patient IDs from system
    patient_ids = [patient.id for patient in system._patients.values()]
    if not patient_ids:
        print("Warning: No patients for appointment initialization")
        return
    
    # Create appointments for the next 14 days
    for i in range(1, 15):
        appt_date = date.today() + timedelta(days=i)
        
        # Morning appointments
        if i % 3 != 0:  # Skip every third day for variety
            appointment1 = Appointment(
                patient_id=patient_ids[i % len(patient_ids)],
                doctor_id=doctor1_id,
                date=appt_date,
                time=time(9, 0)
            )
            system.add_appointment(appointment1)
            
            appointment2 = Appointment(
                patient_id=patient_ids[(i + 2) % len(patient_ids)],
                doctor_id=doctor2_id,
                date=appt_date,
                time=time(10, 30)
            )
            system.add_appointment(appointment2)
        
        # Afternoon appointments
        if i % 2 == 0:  # Every other day
            appointment3 = Appointment(
                patient_id=patient_ids[(i + 1) % len(patient_ids)],
                doctor_id=doctor1_id if i % 2 == 0 else doctor2_id,
                date=appt_date,
                time=time(14, 0)
            )
            system.add_appointment(appointment3)
    
    # Set some appointments to different statuses
    appointments = list(system._appointments.values())
    if appointments:
        appointments[0].update_status("completed")
        if len(appointments) > 1:
            appointments[1].update_status("cancelled")
        if len(appointments) > 3:
            appointments[3].update_status("no-show")

def register_blueprints(app, system, bcrypt):
    from routes.auth import auth_bp, init_auth_routes
    from routes.users import users_bp, init_users_routes
    from routes.patients import patients_bp, init_patients_routes
    from routes.inventory import inventory_bp, init_inventory_routes
    from routes.appointments import appointments_bp, init_appointments_routes
    from routes.medications import medications_bp, init_medications_routes
    from routes.financials import financials_bp, init_financials_routes

    init_auth_routes(auth_bp, system, bcrypt)
    init_users_routes(users_bp, system)
    init_patients_routes(patients_bp, system)
    init_inventory_routes(inventory_bp, system)
    init_appointments_routes(appointments_bp, system)
    init_medications_routes(medications_bp, system)
    init_financials_routes(financials_bp, system)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(medications_bp)
    app.register_blueprint(financials_bp)

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request", "message": str(e)}), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource"}), 403
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found", "message": "The requested resource was not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Server error", "message": "An internal server error occurred"}), 500

# Create and run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    # For WSGI servers
    app = create_app()
