from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from models.reservation_model import Reservation
from config import config

from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if  current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
                return render_template('auth/login.html')
        else:
            flash('User not found')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/reservations', methods=["GET"])
@login_required
def list_reservations():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    cursor = db.connection.cursor()
    reservations = Reservation.get_all(cursor)
    cursor.close()
    print(current_user.fullname)
    return render_template('reservations/list.html', reservations=reservations)

@app.route('/reservations/add', methods=["GET", "POST"])
@login_required
def add():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    cursor = db.connection.cursor()
    return render_template('reservations/form.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '<h1>Pagina no encontrada</h1>', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
