from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm
from application.auth.queries import get_user
from sqlalchemy import update

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	if request.method == "GET":
		return render_template("auth/loginform.html", form = LoginForm())

	form = LoginForm(request.form)
	if not form.validate():
		return render_template("auth/loginform.html", form = form)

	user = get_user(form.username.data)
	if not user:
		return render_template("auth/loginform.html", form = form, no_such_user_error = True)

	user = get_user(form.username.data, form.password.data)
	if not user:
		return render_template("auth/loginform.html", form = form, wrong_password_error = True)

	login_user(user)
	return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
	if request.method == "GET":
		return render_template("auth/registerform.html", form = RegisterForm())

	form = RegisterForm(request.form)
	if not form.validate():
		return render_template("auth/registerform.html", form = form)

	user = get_user(form.username.data)
	if user:
		return render_template("auth/registerform.html", form = form, existing_user_error = True )
	
	user = User(form.username.data, form.password.data)
	db.session().add(user)
	db.session().commit()
	login_user(user)

	return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))
