from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kersa-school-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///school.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import models
from models import User, Student, Teacher, Announcement, Attendance, Exam, Message

# Create database tables
with app.app_context():
    db.create_all()
    # Create admin user if not exists
    if not User.query.filter_by(email='admin@kersaschool.edu.et').first():
        admin = User(
            name='Admin',
            email='admin@kersaschool.edu.et',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: admin@kersaschool.edu.et / admin123")

# ============ AUTH ROUTES ============
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            role=data.get('role', 'student'),
            grade=data.get('grade'),
            section=data.get('section'),
            subject=data.get('subject'),
            phone=data.get('phone')
        )
        db.session.add(user)
        db.session.commit()
        
        # Create token
        token = create_access_token(identity=user.id)
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200

# ============ STUDENT ROUTES ============
@app.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@app.route('/api/students', methods=['POST'])
@jwt_required()
def add_student():
    data = request.json
    try:
        student = Student(
            name=data['name'],
            grade=data['grade'],
            section=data['section'],
            parent_contact=data.get('parent_contact'),
            parent_email=data.get('parent_email'),
            student_id=f"KSS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted'}), 200
    return jsonify({'error': 'Student not found'}), 404

# ============ TEACHER ROUTES ============
@app.route('/api/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers]), 200

@app.route('/api/teachers', methods=['POST'])
@jwt_required()
def add_teacher():
    data = request.json
    try:
        teacher = Teacher(
            name=data['name'],
            subject=data['subject'],
            email=data.get('email'),
            phone=data.get('phone'),
            qualification=data.get('qualification')
        )
        db.session.add(teacher)
        db.session.commit()
        return jsonify(teacher.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ ANNOUNCEMENT ROUTES ============
@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.order_by(Announcement.date.desc()).all()
    return jsonify([a.to_dict() for a in announcements]), 200

@app.route('/api/announcements', methods=['POST'])
@jwt_required()
def add_announcement():
    data = request.json
    try:
        announcement = Announcement(
            title=data['title'],
            content=data['content'],
            priority=data.get('priority', 'medium'),
            user_id=get_jwt_identity()
        )
        db.session.add(announcement)
        db.session.commit()
        return jsonify(announcement.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ ATTENDANCE ROUTES ============
@app.route('/api/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.json
    try:
        attendance = Attendance(
            student_id=data['student_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            status=data['status'],
            reason=data.get('reason'),
            marked_by=get_jwt_identity()
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify(attendance.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    attendance = Attendance.query.filter_by(student_id=student_id).all()
    return jsonify([a.to_dict() for a in attendance]), 200

# ============ AI ROUTES ============
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    from ai.murad_ai import MuradAI
    data = request.json
    message = data.get('message', '')
    
    ai = MuradAI()
    response = ai.get_response(message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/ai/ask', methods=['POST'])
def ai_ask():
    from ai.murad_ai import MuradAI
    data = request.json
    question = data.get('question', '')
    
    ai = MuradAI()
    answer = ai.answer_question(question)
    
    return jsonify({
        'answer': answer,
        'confidence': 0.95,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============ SERVE REACT FRONTEND ============
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
