from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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
from datetime import date, time, datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this in production

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# In-memory user storage
users = []

# Add default admin user
hashed_password = bcrypt.generate_password_hash("password").decode('utf-8')
admin_user = User(1, "Admin", hashed_password, "admin")
admin_user.add_access_permission("Inventory", "/inventory")
admin_user.add_access_permission("Patient", "/patient")
admin_user.add_access_permission("Main", "/main")
users.append(admin_user)

# Add tasks
admin_user.add_task(Task(1, "Task 1", "This is task 1"))
admin_user.add_task(Task(2, "Task 2", "This is task 2"))
admin_user.add_task(Task(3, "Task 3", "This is task 3"))

# Add weekly tasks
admin_user.add_weekly_task(Task(1, "Weekly Task 1", "This is weekly task 1"))
admin_user.add_weekly_task(Task(2, "Weekly Task 2", "This is weekly task 2"))

# Add emergency task
admin_user.add_emergency_task(Task(1, "Emergency Task 1", "This is emergency task 1"))
users.append(admin_user)

doctor1_user = User(2, "Doctor1", hashed_password, "doctor")
doctor1_user.add_access_permission("Patient", "/patient")
doctor1_user.add_access_permission("Main", "/main")
users.append(doctor1_user)

doctor1_user.add_task(Task(1, "Follow-Up", "Mr. Napaul HIV checkup"))
doctor1_user.add_task(Task(2, "Prescribe", "Mr. Bento paracetamol prescription"))

doctor1_user.add_weekly_task(Task(1, "Seminar @BKK", "Trans people seminar"))

doctor2_user = User(3, "Doctor2", hashed_password, "doctor")
doctor2_user.add_access_permission("Patient", "/patient")
doctor2_user.add_access_permission("Main", "/main")
users.append(doctor2_user)

doctor2_user.add_task(Task(1, "Follow-Up", "Mr. Sandwich toothache checkup"))
doctor2_user.add_emergency_task(Task(1, "Euthanization", "Smoke you know who"))

# Add Receptionists
receptionist1_user = User(4, "Sally Smith", hashed_password, "Receptionist")  
receptionist2_user = User(5, "Megan Bright", hashed_password, "Receptionist")  
receptionist3_user = User(6, "Tina Turner", hashed_password, "Receptionist")  

# Add patient
patient1 = Patient("Nuker Ducker",12,"Male","duckyduck@haha.com")
patient2 = Patient("Nhow Socool",36,"Male","Cold@weather.com")
patient3 = Patient("Eat Bento", 99,"Male","Hungry@Calories.com")
patient4 = Patient("Cheesy Sandwich", 20, "Male", "Expired@farm.com")
patient5 = Patient("Nobi Nobitata", 10, "Male", "Need@doraemon.com")
patient6 = Patient("Sir Render", 40, "Male", "Glitch@graphics.com")  
patient7 = Patient("Anna Conda", 22, "Female", "Snake@hiss.com")  
patient8 = Patient("Karen Outage", 45, "Female", "Manager@now.com") 
patient9 = Patient("Polly Graph", 32, "Female", "Data@charts.com")
patient10 = Patient("Rita Book", 24, "Female", "Quiet@library.com")

# Add Prescription to patients
patient1.add_prescription(Prescription(1, 2, "Duckamine", "10mg, once daily", 1.5))  
patient2.add_prescription(Prescription(2, 3, "Coolantol", "5mg, twice daily", 2.0))  
patient3.add_prescription(Prescription(3, 2, "Bentoformin", "20mg, after meals", 3.2))  
patient4.add_prescription(Prescription(4, 3, "Cheesadol", "15mg, before bed", 1.8))  
patient5.add_prescription(Prescription(5, 2, "Doramycin", "7.5mg, three times a day", 2.5))  
patient6.add_prescription(Prescription(6, 3, "Pretzaleve", "12mg, as needed", 1.3))  
patient7.add_prescription(Prescription(7, 2, "Koalanol", "5mg, before sleep", 2.1))  
patient8.add_prescription(Prescription(8, 3, "Pepperzin", "10mg, after spicy foods", 1.7))  
patient9.add_prescription(Prescription(9, 2, "Mystiril", "8mg, every 6 hours", 2.9))  
patient10.add_prescription(Prescription(10, 3, "Renderol", "25mg, once daily", 3.0))

# Add medications
patient1.add_medication(Medication(1, "Duckafen", "10mg, once daily", date(2025, 3, 1), date(2025, 3, 15), "May cause excessive quacking."))  
patient2.add_medication(Medication(2, "Coolomax", "5mg, twice daily", date(2025, 2, 20), date(2025, 3, 5), "Keep refrigerated. Might make you chill."))  
patient3.add_medication(Medication(3, "Bentozyme", "20mg, after meals", date(2025, 1, 15), date(2025, 2, 15), "May increase craving for sushi."))  
patient4.add_medication(Medication(4, "Cheesotrin", "15mg, before bed", date(2025, 3, 10), date(2025, 4, 10), "May cause dreams about dairy."))  
patient5.add_medication(Medication(5, "Doraflex", "7.5mg, three times a day", date(2025, 1, 5), date(2025, 2, 5), "Not a time machine, sorry."))  
patient6.add_medication(Medication(6, "Pretzolax", "12mg, as needed", date(2025, 2, 10), date(2025, 3, 10), "May cause a craving for mustard."))  
patient7.add_medication(Medication(7, "Koalasleep", "5mg, before sleep", date(2025, 3, 1), date(2025, 3, 21), "May induce tree-hugging urges."))  
patient8.add_medication(Medication(8, "Pepperprol", "10mg, after spicy foods", date(2025, 1, 25), date(2025, 2, 25), "Might make you sneeze less."))  
patient9.add_medication(Medication(9, "Mysticil", "8mg, every 6 hours", date(2025, 2, 1), date(2025, 2, 28), "May reveal hidden secrets."))  
patient10.add_medication(Medication(10, "Renderin", "25mg, once daily", date(2025, 2, 15), date(2025, 3, 15), "May cause pixelation of reality."))

# Add treatments
patient1.add_treatment(Treatment("Headache and dizziness", "Migraine", "Prescribed sumatriptan and advised rest", date(2025, 3, 5), True))  
patient2.add_treatment(Treatment("Shortness of breath", "Mild asthma", "Inhaler prescribed and advised to avoid allergens", date(2025, 2, 12), False))  
patient3.add_treatment(Treatment("Abdominal pain", "Gastritis", "Prescribed omeprazole and recommended dietary changes", date(2025, 1, 20), True))  
patient4.add_treatment(Treatment("Joint stiffness", "Rheumatoid arthritis", "Started on methotrexate and physical therapy", date(2025, 3, 10), False))  
patient5.add_treatment(Treatment("Fatigue and weight loss", "Hyperthyroidism", "Prescribed carbimazole and scheduled follow-up", date(2025, 1, 25), True))  
patient6.add_treatment(Treatment("Skin rash and itching", "Eczema", "Prescribed corticosteroid cream and antihistamines", date(2025, 2, 15), False))  
patient7.add_treatment(Treatment("Fever and sore throat", "Strep throat", "Prescribed amoxicillin and advised rest", date(2025, 3, 3), True))  
patient8.add_treatment(Treatment("Chest pain", "Costochondritis", "Prescribed ibuprofen and advised stretching exercises", date(2025, 1, 10), True))  
patient9.add_treatment(Treatment("Insomnia", "Generalized anxiety disorder", "Prescribed lorazepam and referred to counseling", date(2025, 2, 5), False))  
patient10.add_treatment(Treatment("Blurred vision and eye pain", "Optic neuritis", "Started on corticosteroids and referred to ophthalmology", date(2025, 2, 20), True))  

# Add fees
patient1.add_fee(Fee(1, 150.00, "doctor", "Consultation with general practitioner", "2025-03-05"))  
patient2.add_fee(Fee(2, 45.50, "medication", "Inhaler prescription", "2025-02-12"))  
patient3.add_fee(Fee(3, 120.75, "lab", "Blood test for gastritis diagnosis", "2025-01-20"))  
patient4.add_fee(Fee(4, 200.00, "doctor", "Rheumatology consultation", "2025-03-10"))  
patient5.add_fee(Fee(5, 80.25, "medication", "Carbimazole prescription", "2025-01-25"))  
patient6.add_fee(Fee(6, 60.00, "lab", "Skin biopsy for eczema", "2025-02-15"))  
patient7.add_fee(Fee(7, 100.00, "doctor", "Pediatric consultation for strep throat", "2025-03-03"))  
patient8.add_fee(Fee(8, 30.00, "medication", "Ibuprofen prescription", "2025-01-10"))  
patient9.add_fee(Fee(9, 250.00, "other", "Counseling session for anxiety", "2025-02-05"))  
patient10.add_fee(Fee(10, 180.00, "doctor", "Ophthalmology consultation", "2025-02-20")) 

drug1 = Supply("Paracetamol", 200, 0.50, "Pain Relief")  
drug2 = Supply("Amoxicillin", 500, 0.30, "Antibiotic")  
drug3 = Supply("Insulin", 100, 5.00, "Diabetes Management")  
drug4 = Supply("Ibuprofen", 300, 1.20, "Pain Relief")  
drug5 = Supply("Cough Syrup", 250, 0.40, "Cold & Flu")  
drug6 = Supply("Antihistamine", 50, 15.00, "Allergy Relief")  
drug7 = Supply("Blood Pressure Medication", 30, 25.00, "Cardiovascular")  
drug8 = Supply("Antacid", 400, 0.10, "Digestive Health")  
drug9 = Supply("Epinephrine", 150, 0.75, "Emergency Allergy Treatment")  
drug10 = Supply("Sleeping Pills", 100, 2.50, "Sleep Aid")  


# Add tasks to doctor so they overwork
doctor1_user.add_task(Task(3, "Patient Consultation", "Ms. Pepperoni experiencing heartburn"))  
doctor1_user.add_task(Task(4, "Physical Exam", "Routine checkup for Mr. Treadmill"))  

doctor1_user.add_emergency_task(Task(1, "Code Blue", "Emergency resuscitation for Mr. Lightning"))  

doctor1_user.add_weekly_task(Task(2, "Staff Meeting", "Discuss new hospital protocols"))

doctor2_user.add_task(Task(2, "Annual Physical", "Routine checkup for Mr. Nuker Ducker"))  
doctor2_user.add_task(Task(3, "Diet Consultation", "Help Mr. Eat Bento with high cholesterol"))  
doctor2_user.add_task(Task(4, "Vision Test", "Check Ms. Polly Graph's eyesight"))  
doctor2_user.add_task(Task(5, "Blood Work Review", "Discuss test results with Mr. Nhow Socool"))  
doctor2_user.add_task(Task(6, "Allergy Test", "Determine cause of rash for Ms. Anna Conda"))  

doctor2_user.add_emergency_task(Task(2, "Severe Allergic Reaction", "Ms. Karen Outage in anaphylactic shock"))  
doctor2_user.add_emergency_task(Task(3, "Cardiac Arrest", "Mr. Sir Render experiencing heart failure"))  

doctor2_user.add_weekly_task(Task(1, "Department Meeting", "Review monthly performance and improvements")) 

#add patient history entry
patient1.add_history_entry("2015-06-12: Nuker Ducker suffered a mysterious case of excessive quacking during a swim, later diagnosed as a mild allergy to rubber duckies.")  
patient2.add_history_entry("2018-11-22: Nhow Socool visited due to an intense cold front, diagnosed with 'Too Much Coolness' — prescribed a blanket and a hot cup of tea.")  
patient3.add_history_entry("2010-08-05: Eat Bento complained of 'chronic hunger.' Diagnosed with severe appetite, prescribed sushi for lunch.")  
patient4.add_history_entry("2020-05-17: Cheesy Sandwich presented with 'too many cheesy puns.' Diagnosed with a cheese overload. Treatment: Take a break from dad jokes.")  
patient5.add_history_entry("2017-09-30: Nobi Nobitata arrived with a case of 'missing gadgets.' Diagnosed with Doreamonitis — prescribed a temporary replacement gadget, Doraemon-style.")  

patients = []
try:
    # Create 5 patients with different conditions and histories
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
    
    # Add lab results to patients
    from modules.lab_result import LabResult
    lab1 = LabResult(patient1.id, "Complete Blood Count", "Normal range", date.today() - timedelta(days=15))
    lab2 = LabResult(patient1.id, "Metabolic Panel", "Glucose: 105 mg/dL (slightly elevated)", date.today() - timedelta(days=15))
    patient1.add_lab_result(lab1)
    patient1.add_lab_result(lab2)
    
    lab3 = LabResult(patient2.id, "Pregnancy Glucose Test", "Normal", date.today() - timedelta(days=28))
    lab4 = LabResult(patient2.id, "Iron Level", "Slightly low - recommend supplements", date.today() - timedelta(days=28))
    patient2.add_lab_result(lab3)
    patient2.add_lab_result(lab4)
    
    lab5 = LabResult(patient3.id, "HbA1c", "7.2% - Improved from previous test", date.today() - timedelta(days=45))
    lab6 = LabResult(patient3.id, "Lipid Panel", "Total Cholesterol: 210 mg/dL", date.today() - timedelta(days=45))
    patient3.add_lab_result(lab5)
    patient3.add_lab_result(lab6)
    
    # Add medications to patients
    med1 = Medication(patient1.id, "Naproxen", "500mg twice daily", 
                     date.today() - timedelta(days=60), date.today() + timedelta(days=30),
                     "Take with food to avoid stomach upset")
    patient1.add_medication(med1)
    
    med2 = Medication(patient2.id, "Prenatal Vitamins", "One tablet daily", 
                     date.today() - timedelta(days=90), date.today() + timedelta(days=150),
                     "Contains folic acid and iron")
    patient2.add_medication(med2)
    
    med3 = Medication(patient3.id, "Metformin", "500mg with breakfast and dinner", 
                     date.today() - timedelta(days=180), date.today() + timedelta(days=185),
                     "Long-term medication for diabetes management")
    patient3.add_medication(med3)
    
    med4 = Medication(patient4.id, "Sertraline", "50mg daily in the morning", 
                     date.today() - timedelta(days=25), date.today() + timedelta(days=95),
                     "May take 2-4 weeks to feel full effects")
    patient4.add_medication(med4)
    
    med5 = Medication(patient5.id, "Lisinopril", "10mg daily", 
                     date.today() - timedelta(days=165), date.today() + timedelta(days=200),
                     "Monitor blood pressure weekly")
    patient5.add_medication(med5)
    
    # Add fees to patients
    from modules.fee import Fee
    fee1 = Fee(patient1.id, 150.00, "Office visit", date.today() - timedelta(days=15))
    fee2 = Fee(patient1.id, 75.00, "Blood work", date.today() - timedelta(days=15))
    patient1.add_fee(fee1)
    patient1.add_fee(fee2)
    
    fee3 = Fee(patient2.id, 200.00, "Prenatal checkup", date.today() - timedelta(days=28))
    fee4 = Fee(patient2.id, 350.00, "Ultrasound", date.today() - timedelta(days=28))
    patient2.add_fee(fee3)
    patient2.add_fee(fee4)
    
    fee5 = Fee(patient3.id, 125.00, "Follow-up visit", date.today() - timedelta(days=45))
    fee6 = Fee(patient3.id, 95.00, "HbA1c test", date.today() - timedelta(days=45))
    patient3.add_fee(fee5)
    patient3.add_fee(fee6)
    
except Exception as e:
    print(f"Error creating mock patients: {str(e)}")

# Create mock supplies
supplies = []
try:
    supplies.append(Supply("Examination Gloves (Box of 100)", 50, 8.99, "Protective Equipment"))
    supplies.append(Supply("Surgical Masks (Box of 50)", 30, 12.50, "Protective Equipment"))
    supplies.append(Supply("Alcohol Swabs (Pack of 100)", 45, 5.25, "Sterilization"))
    supplies.append(Supply("Blood Pressure Cuffs", 15, 45.99, "Diagnostic Equipment"))
    supplies.append(Supply("Digital Thermometers", 25, 18.75, "Diagnostic Equipment"))
    supplies.append(Supply("Syringes 5ml (Box of 100)", 20, 22.50, "Injection Supplies"))
    supplies.append(Supply("Bandages (Box of 50)", 35, 7.99, "Wound Care"))
    supplies.append(Supply("Gauze Pads 4x4 (Pack of 200)", 28, 15.50, "Wound Care"))
    supplies.append(Supply("Hand Sanitizer (1 Liter)", 40, 9.25, "Hygiene Products"))
    supplies.append(Supply("Patient Gowns", 60, 6.50, "Patient Care"))
except Exception as e:
    print(f"Error creating mock supplies: {str(e)}")

# Create mock appointments
appointments = []
try:
    # Create appointments for the next 14 days
    for i in range(1, 15):
        appt_date = date.today() + timedelta(days=i)
        
        # Morning appointments
        if i % 3 != 0:  # Skip every third day for variety
            appointments.append(Appointment(
                patient1.id if i % 5 == 1 else (patient2.id if i % 5 == 2 else (patient3.id if i % 5 == 3 else (patient4.id if i % 5 == 4 else patient5.id))),
                doctor1_user.id,
                appt_date,
                time(9, 0)
            ))
            
            appointments.append(Appointment(
                patient5.id if i % 5 == 1 else (patient4.id if i % 5 == 2 else (patient3.id if i % 5 == 3 else (patient2.id if i % 5 == 4 else patient1.id))),
                doctor2_user.id,
                appt_date,
                time(10, 30)
            ))
        
        # Afternoon appointments
        if i % 2 == 0:  # Every other day
            appointments.append(Appointment(
                patient2.id if i % 5 == 1 else (patient3.id if i % 5 == 2 else (patient4.id if i % 5 == 3 else (patient5.id if i % 5 == 4 else patient1.id))),
                doctor1_user.id if i % 2 == 0 else doctor2_user.id,
                appt_date,
                time(14, 0)
            ))
    
    # Set some appointments to different statuses
    appointments[0].update_status("completed")
    appointments[1].update_status("cancelled")
    appointments[3].update_status("no-show")
except Exception as e:
    print(f"Error creating mock appointments: {str(e)}")

# --------------------------------
# API ENDPOINTS FOR MOCK DATA
# --------------------------------

@app.route('/api/patients', methods=['GET'])
@jwt_required()
def get_patients():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all patients
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'age': p.age,
        'gender': p.gender,
        'contact': p.contact,
        'history': p.history,
        'lab_results_count': len(p.get_lab_results()),
        'medications_count': len(p.get_medications()),
        'current_medications_count': len(p.current_medications),
        'fees_total': p.calculate_total_fees()
    } for p in patients]), 200

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Find patient by ID
    patient = next((p for p in patients if p.id == patient_id), None)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(patient.get_report_data()), 200

@app.route('/api/supplies', methods=['GET'])
@jwt_required()
def get_supplies():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check - only admin can see supplies
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all supplies
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'quantity': s.quantity,
        'unit_price': s.unit_price,
        'category': s.category,
        'total_value': s.total_value()
    } for s in supplies]), 200

@app.route('/api/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # For doctors, only return their appointments
    filtered_appointments = appointments
    if user.user_type == "doctor":
        filtered_appointments = [a for a in appointments if a.doctor_id == user.id]
    
    # Return appointments
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'patient_name': next((p.name for p in patients if p.id == a.patient_id), "Unknown"),
        'doctor_id': a.doctor_id,
        'doctor_name': next((u.username for u in users if u.id == a.doctor_id), "Unknown"),
        'date': a.date.isoformat(),
        'time': a.time.isoformat(),
        'status': a.status
    } for a in filtered_appointments]), 200

@app.route('/api/medications', methods=['GET'])
@jwt_required()
def get_medications():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Collect all medications from all patients
    all_medications = []
    for patient in patients:
        medications = patient.get_medications()
        for med in medications:
            all_medications.append({
                'id': med.id,
                'patient_id': med.patient_id,
                'patient_name': next((p.name for p in patients if p.id == med.patient_id), "Unknown"),
                'name': med.name,
                'dosage': med.dosage,
                'start_date': med.start_date.isoformat(),
                'end_date': med.end_date.isoformat(),
                'notes': med.notes,
                'active': med.active,
                'finished': med.finished
            })
    
    return jsonify(all_medications), 200

# Helper function to find user by username
def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

# Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    if find_user_by_username(username):
        return jsonify({"error": "Username already taken"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = len(users) + 1  # Simple ID generation
    new_user = User(user_id, username, hashed_password)
    users.append(new_user)

    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token - store just the username as identity
    access_token = create_access_token(identity=user.username)
    print(f"User {user.username} logged in")
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

# Protected Route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_username = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_username}! This is a protected route."}), 200

@app.route('/api/user-data', methods=['GET'])
@jwt_required()
def get_user_data():
    current_username = get_jwt_identity()  # This is now just the username string
    user = find_user_by_username(current_username)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Only allow admin to see all users
    current_username = get_jwt_identity()  # This is now just the username string
    user = find_user_by_username(current_username)
    
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify([u.to_dict() for u in users])

# Add a new inventory item
@app.route('/api/inventory/add', methods=['POST'])
@jwt_required()
def add_inventory():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Create new supply with the provided data
        new_supply = Supply(
            data.get('name'),
            int(data.get('quantity')),
            float(data.get('unit_price')),
            data.get('category')
        )
        
        # Add to our supplies list
        supplies.append(new_supply)
        
        return jsonify({
            'message': 'Inventory item added successfully',
            'id': new_supply.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Update an existing inventory item
@app.route('/api/inventory/update', methods=['PUT'])
@jwt_required()
def update_inventory():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item_id = data.get('id')
    
    try:
        # Find the supply item
        supply_item = next((s for s in supplies if s.id == item_id), None)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Update the supply item properties
        supply_item.name = data.get('name')
        supply_item.quantity = int(data.get('quantity'))
        supply_item.unit_price = float(data.get('unit_price'))
        supply_item.category = data.get('category')
        
        return jsonify({
            'message': 'Inventory item updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Add count to an inventory item
@app.route('/api/inventory/add-count', methods=['POST'])
@jwt_required()
def add_count():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item_id = data.get('inventoryId')
    count = int(data.get('count'))
    
    try:
        # Find the supply item
        supply_item = next((s for s in supplies if s.id == item_id), None)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Add count
        supply_item.quantity += count
        
        return jsonify({
            'message': 'Count added successfully',
            'new_count': supply_item.quantity
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete count from an inventory item
@app.route('/api/inventory/delete-count', methods=['POST'])
@jwt_required()
def delete_count():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item_id = data.get('inventoryId')
    count = int(data.get('count'))
    
    try:
        # Find the supply item
        supply_item = next((s for s in supplies if s.id == item_id), None)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Delete count, ensuring it doesn't go below zero
        supply_item.quantity = max(0, supply_item.quantity - count)
        
        return jsonify({
            'message': 'Count deleted successfully',
            'new_count': supply_item.quantity
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --------------------------------
# API ENDPOINTS FOR PATIENT MANAGEMENT
# --------------------------------

@app.route('/api/patients/add', methods=['POST'])
@jwt_required()
def add_patient():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    try:
        # Create new patient with the provided data
        new_patient = Patient(
            data.get('name'),
            int(data.get('age')),
            data.get('gender'),
            data.get('contact')
        )
        
        # Add to our patients list
        patients.append(new_patient)
        
        return jsonify({
            'message': 'Patient added successfully',
            'id': new_patient.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/update', methods=['PUT'])
@jwt_required()
def update_patient():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    patient_id = data.get('id')
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Update only allowed fields based on role
        if user.user_type in ["admin", "receptionist"]:
            # Admin and receptionist can update all patient info
            patient._name = data.get('name')
            patient._age = int(data.get('age'))
            patient._gender = data.get('gender')
            patient._contact = data.get('contact')
        elif user.user_type == "doctor":
            # Doctors can only update medical information, not personal info
            pass
        
        return jsonify({
            'message': 'Patient updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/delete/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check - only admin can delete patients
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the patient
        patient_index = next((i for i, p in enumerate(patients) if p.id == patient_id), None)
        
        if patient_index is None:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Remove the patient
        patients.pop(patient_index)
        
        return jsonify({
            'message': 'Patient deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/<int:patient_id>/history', methods=['POST'])
@jwt_required()
def add_patient_history(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    entry = data.get('entry')
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Add history entry
        result, message = patient.add_history_entry(entry)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Fees management endpoints for receptionist

@app.route('/api/patients/<int:patient_id>/fees', methods=['POST'])
@jwt_required()
def add_patient_fee(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Create new fee
        from modules.fee import Fee
        new_fee = Fee(
            patient_id,
            float(data.get('amount')),
            data.get('description'),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today()
        )
        
        # Add fee to patient
        result, message = patient.add_fee(new_fee)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message,
            'fee_id': new_fee.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/<int:patient_id>/fees/<int:fee_id>', methods=['PUT'])
@jwt_required()
def update_patient_fee(patient_id, fee_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get the existing fee
        existing_fee = patient.get_fee(fee_id)
        if not existing_fee:
            return jsonify({'error': 'Fee not found'}), 404
        
        # Create updated fee
        from modules.fee import Fee
        updated_fee = Fee(
            patient_id,
            float(data.get('amount')),
            data.get('description'),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else existing_fee.date
        )
        updated_fee.id = fee_id  # Keep the same ID
        
        # Update fee
        result, message = patient.update_fee(fee_id, updated_fee)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/<int:patient_id>/fees/<int:fee_id>', methods=['DELETE'])
@jwt_required()
def delete_patient_fee(patient_id, fee_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Delete fee
        result, message = patient.remove_fee(fee_id)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Financial report endpoint for receptionist
@app.route('/api/financial-report', methods=['GET'])
@jwt_required()
def get_financial_report():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    try:
        # For demonstration, we'll use the system's generate_financial_report method
        success, report = system.generate_financial_report(start_date, end_date)
        
        if not success:
            return jsonify({'error': 'Failed to generate report'}), 400
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --------------------------------
# API ENDPOINTS FOR APPOINTMENTS
# --------------------------------

@app.route('/api/appointments/add', methods=['POST'])
@jwt_required()
def add_appointment():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Create new appointment
        from modules.appointment import Appointment
        new_appointment = Appointment(
            int(data.get('patient_id')),
            int(data.get('doctor_id')),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            datetime.strptime(data.get('time'), '%H:%M').time()
        )
        
        # Add to appointments list
        appointments.append(new_appointment)
        
        return jsonify({
            'message': 'Appointment added successfully',
            'id': new_appointment.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/appointments/update', methods=['PUT'])
@jwt_required()
def update_appointment():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    appointment_id = data.get('id')
    
    try:
        # Find the appointment
        appointment = next((a for a in appointments if a.id == appointment_id), None)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update appointment fields
        appointment.patient_id = int(data.get('patient_id'))
        appointment.doctor_id = int(data.get('doctor_id'))
        appointment.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        appointment.time = datetime.strptime(data.get('time'), '%H:%M').time()
        
        if data.get('status'):
            appointment.update_status(data.get('status'))
        
        return jsonify({
            'message': 'Appointment updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/appointments/delete/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the appointment
        appointment_index = next((i for i, a in enumerate(appointments) if a.id == appointment_id), None)
        
        if appointment_index is None:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Remove the appointment
        appointments.pop(appointment_index)
        
        return jsonify({
            'message': 'Appointment deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/appointments/status/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    status = data.get('status')
    
    try:
        # Find the appointment
        appointment = next((a for a in appointments if a.id == appointment_id), None)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update status
        appointment.update_status(status)
        
        return jsonify({
            'message': 'Appointment status updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Create a System instance for receptionist functionality
from modules.system import System
system = System()

# Add existing patients to the system
for patient in patients:
    system.add_patient(patient)

if __name__ == '__main__':
    app.run(debug=True)
