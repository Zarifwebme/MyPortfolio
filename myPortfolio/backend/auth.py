import os
from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, render_template, flash

auth_bp = Blueprint("auth", __name__)


def login_required(view_func):
	@wraps(view_func)
	def wrapped(*args, **kwargs):
		if not session.get("admin_logged_in"):
			return redirect(url_for("auth.login"))
		return view_func(*args, **kwargs)
	return wrapped


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username", "")
		password = request.form.get("password", "")
		if username == os.getenv("ADMIN_USERNAME", "admin") and password == os.getenv("ADMIN_PASSWORD", "admin"):
			session["admin_logged_in"] = True
			flash("Logged in successfully", "success")
			return redirect(url_for("admin.dashboard"))
		flash("Invalid credentials", "danger")
	return render_template("admin/login.html")


@auth_bp.get("/logout")
@login_required
def logout():
	session.clear()
	flash("Logged out", "info")
	return redirect(url_for("auth.login"))
