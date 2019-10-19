from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_login import LoginManager , login_required , UserMixin , login_user
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/sherlock/Desktop/CENG/scoreboard/score.db'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'b\xc1<\x9f]H\xfar\t[\x96\x07YG\xc8\xe4Q\xc43#\xdc\xe5E\xf5\xd9'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True,autoincrement=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return redirect(url_for('index'))



@app.route("/complete/<string:id>")
def completeScore(id):
    lastversion=score.query.filter_by(id=id).first()
    lastversion.complete=not lastversion.complete

    db.session.commit()
    return redirect(url_for("index"))
@app.route("/")
def index():
    scores=score.query.all()
    return render_template("index.html",scores=scores)

@app.route("/add",methods=["POST"])
def addScore():
    title=request.form.get("title")
    newScore=score(title=title,complete=False)
    db.session.add(newScore)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteScoreId(id):
    lastversion=score.query.filter_by(id=id).first()
    db.session.delete(lastversion)
    db.session.commit()
    return redirect(url_for("index"))




@app.route('/viewonly', methods=['GET', 'POST'])
def viewonly():
    scores=score.query.all()
    return render_template('viewonly.html',scores=scores)

class score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    complete=db.Column(db.Boolean)

class LoginForm(Form):
    username=StringField("Kullanici Adi")
    password=PasswordField("Parola")


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)


