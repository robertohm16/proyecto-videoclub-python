from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

# Definicion de las tablas
class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

class Movie(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    duration = db.Column(db.String(250), nullable=False)
    release_year = db.Column(db.String(250), nullable=False)
    director = db.Column(db.String(250), nullable=False)
    Actors = db.Column(db.String(250), nullable=False)
    Rating = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
	db.create_all()


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


def add_movie(title, genero, duration, release_year, director, actors, rating):
    movie = Movie(title=title, genero=genero, duration=duration, release_year=release_year, director=director, actors=actors, rating=rating)
    db.session.add(movie)
    db.session.commit()

def update_movie(movie_id, title, genero, duration, release_year, director, actors, rating):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.title = title
        movie.genero = genero
        movie.duration = duration
        movie.release_year = release_year
        movie.director = director
        movie.actors = actors
        movie.rating = rating
        db.session.commit()
        return True
    return False

def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return True
    return False

def list_movies():
    return Movie.query.all()


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Validar que los campos no estén vacíos
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("sign_up.html")

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
        else:
            if username.strip() and password.strip():  # Verificar que no sean cadenas vacías después de eliminar espacios en blanco
                user = Users(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                flash('Username and password cannot be empty', 'error')
                return render_template("sign_up.html")
    return render_template("sign_up.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route("/users")
def list_users():
    users = Users.query.all()
    return render_template("list_users.html", users=users)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/")
def home():
	return render_template("home.html")



if __name__ == "__main__":
    app.run(debug =True, port=4000)