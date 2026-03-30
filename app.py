from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from models import Student, Attendance
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')
    
    if name and roll_number:
        # Check if student already exists
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            flash('Student with this roll number already exists!', 'danger')
        else:
            student = Student(name=name, roll_number=roll_number)
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
    
    return redirect(url_for('students'))

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        status = request.form.get('status')
        date_str = request.form.get('date')
        
        if student_id and status:
            # Parse date
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date = datetime.now().date()
            
            # Check if attendance already marked for this date
            existing = Attendance.query.filter_by(
                student_id=student_id, 
                date=date
            ).first()
            
            if existing:
                flash('Attendance already marked for this date!', 'warning')
            else:
                attendance = Attendance(
                    student_id=student_id,
                    date=date,
                    status=status
                )
                db.session.add(attendance)
                db.session.commit()
                flash('Attendance marked successfully!', 'success')
    
    students = Student.query.all()
    return render_template('mark_attendance.html', students=students)

@app.route('/attendance_report')
def attendance_report():
    students = Student.query.all()
    attendance_data = []
    
    for student in students:
        total_classes = Attendance.query.filter_by(student_id=student.id).count()
        present_count = Attendance.query.filter_by(
            student_id=student.id, 
            status='Present'
        ).count()
        
        attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        attendance_data.append({
            'student': student,
            'total_classes': total_classes,
            'present_count': present_count,
            'attendance_percentage': round(attendance_percentage, 2)
        })
    
    return render_template('attendance_report.html', attendance_data=attendance_data)

@app.route('/check_attendance', methods=['GET', 'POST'])
def check_attendance():
    result = None
    minimum_percentage = 75  # Default minimum attendance requirement
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        min_percentage = float(request.form.get('min_percentage', 75))
        
        student = Student.query.get(student_id)
        
        if student:
            total_classes = Attendance.query.filter_by(student_id=student.id).count()
            present_count = Attendance.query.filter_by(
                student_id=student.id, 
                status='Present'
            ).count()
            
            attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
            meets_requirement = attendance_percentage >= min_percentage
            
            result = {
                'student': student,
                'total_classes': total_classes,
                'present_count': present_count,
                'attendance_percentage': round(attendance_percentage, 2),
                'minimum_required': min_percentage,
                'meets_requirement': meets_requirement
            }
    
    students = Student.query.all()
    return render_template('check_attendance.html', students=students, result=result)

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    attendance_records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).all()
    
    total_classes = len(attendance_records)
    present_count = sum(1 for record in attendance_records if record.status == 'Present')
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    return render_template('student_details.html', 
                         student=student, 
                         attendance_records=attendance_records,
                         attendance_percentage=round(attendance_percentage, 2))

if __name__ == '__main__':
    app.run(debug=True)