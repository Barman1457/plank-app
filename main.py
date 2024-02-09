from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    plank_time = db.Column(db.String(10), nullable=False)

# Routes and database operations within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grade_selection', methods=['GET', 'POST'])
def grade_selection():
    if request.method == 'POST':
        grade = request.form['grade']
        return redirect(url_for('plank_time_selection', grade=grade))
    return render_template('grade_selection.html')

@app.route('/plank_time_selection/<int:grade>')
def plank_time_selection(grade):
    plank_times = ['801', '802', '803'] if grade == 8 else ['901', '902', '903'] if grade == 9 else ['701', '702', '703']
    return render_template('plank_time_selection.html', grade=grade, plank_times=plank_times)
@app.route('/student_input/<int:grade>/<plank_time>', methods=['GET', 'POST'])
def student_input(grade, plank_time):
    if request.method == 'POST':
        name = request.form['student_name']
        plank_duration = request.form['plank_duration']

        # Save student data to the database
        student = Student(name=name, grade=grade, plank_time=plank_time)
        db.session.add(student)
        db.session.commit()

    # Fetch students for the selected grade and plank time
    students = Student.query.filter_by(grade=grade, plank_time=plank_time).all()
    return render_template('student_input.html', grade=grade, plank_time=plank_time, students=students)

@app.route('/clear_data/<int:student_id>', methods=['POST'])
def clear_student_data(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
