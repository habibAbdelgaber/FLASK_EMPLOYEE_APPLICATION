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
    emp_list = Employees.query.all()
    
    return render_template('home.html', emp_list=emp_list)


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
    


if __name__ == '__main__':
    app.run(debug=True)
