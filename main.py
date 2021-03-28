from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thismyappsecret'

db = SQLAlchemy(app)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    

    def __init__(self, name, username, age, email):
        self.name = name
        self.username = username
        self.age = age
        self.email = email

    def __str__(self):
        return f"{self.name} {self.username}"



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/employees')
def employees():
    emp_list = Employees.query.all()
    return render_template('employees_list.html', emp_list=emp_list)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        age = request.form['age']
        email = request.form['email']
        employee = Employees(
            name=name,
            username=username,
            age=age,
            email=email
        )

        db.session.add(employee)
        db.session.commit()
        flash('New employee was created successfully!', category='success')
        return redirect(url_for('home'))
    return render_template('create.html')
    
@app.route('/detail/<id>')
def detail(id):
    emp = Employees.query.get(id)
    return render_template('detail.html', emp=emp)

# Update logic goes here!

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    emp = Employees.query.get(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.username = request.form['username']
        emp.age = request.form['age']
        emp.email = request.form['email']
        db.session.commit()
        flash('You updated you information!')
        print(emp)
        return redirect(url_for('employees'))
    return render_template('update.html', emp=emp)
   


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    emp = Employees.query.get(id)
    if request.method == 'POST':
        db.session.delete(emp)
        db.session.commit()
        return redirect(url_for('employees'))
    return render_template('delete.html', emp=emp)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

# Assignment
"""
We have seen how simple is to create Flask application, the micro python Framework.
It works very friendly to create any type of applications that can fills your need.
And as we created our CRUD application for employees, we seen how thing work friendly though we didn't finish yet it remains one logic to finish or to wrap up our app.
Now, we want to extends adding some fields;
1- Add three fields to our database:  a) subject field. b) employee bio field, the employee bio can be displayed only in employee detail.
c) boolean field, adding boolean field to differentiate if the employee is interviewed or not.
Hint! mark some employees as interviewed and some not.
2- All three fields can displayed in employees list except employee bio.
3- Let's make a function that allows employees to update their information if they want or in case they missed something!
''' You make this app more complex if you want for e.g if you want to have different interview sections in same app!'''
# Goodluck!!!
"""
