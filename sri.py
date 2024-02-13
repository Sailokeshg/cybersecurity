import csv
import random
import string
from faker import Faker
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))
fake = Faker()
with open('students.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'Name', 'Email', 'Phonenumber'])
    for i in range(1, 1001):
        studentid = i
        name = fake.name()
        email = fake.email()
        phonenumber = generate_random_phone()
        writer.writerow([studentid, name, email, phonenumber])
app = Flask(__name__)
app.secret_key = 'your_secret_key'  
@app.route('/')
def index():
    students = []
    with open('students.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append(row)
    return render_template('app.html', title='Student Database', students=students)
@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        studentid = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phonenumber = request.form['phonenumber']

        if not studentid.isdigit():
            flash('ID should contain only integers.')
        else:
            studentid = int(studentid)
            with open('students.csv', mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if str(studentid) == row[0]:
                        flash('ID already exists.')
                        return redirect(url_for('addstudent'))
            with open('students.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([studentid, name, email, phonenumber])
            flash('added student.')
            return redirect(url_for('index'))

    return render_template('addstudent.html', title='Add Student')

@app.route('/search_student', methods=['POST'])
def search_student():
    studentid = request.form['search_id']
    student = None
    with open('students.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if studentid == row[0]:
                student = {
                    'id': row[0],
                    'Name': row[1],
                    'Email': row[2],
                    'Phonenumber': row[3]
                }
                break

    if student:
        return render_template('search_result.html', title='Search Result', student=student)
    else:
        return render_template('student_not_found.html', title='Student Not Found')

@app.route('/updatestudent/<int:id>', methods=['GET', 'POST'])
def updatestudent(id):
    students = []
    with open('students.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append(row)
    for student in students:
        if int(student['id']) == id:
            if request.method == 'POST':
                student['Name'] = request.form['name']
                student['Email'] = request.form['email']
                student['Phonenumber'] = request.form['phonenumber']
                with open('students.csv', mode='w', newline='') as file:
                    fieldnames = ['id', 'Name', 'Email', 'Phonenumber']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(students)

                flash('updated student.')
                return redirect(url_for('index'))

            return render_template('updatestudent.html', title='Update Student', student=student)

    flash('Student not found.')
    return redirect(url_for('index'))

@app.route('/deletestudent/<int:id>')
def deletestudent(id):

    students = []
    with open('students.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append(row)

    for student in students:
        if int(student['id']) == id:
            students.remove(student)

            with open('students.csv', mode='w', newline='') as file:
                fieldnames = ['id', 'Name', 'Email', 'Phonenumber']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)

            flash('deleted.')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
