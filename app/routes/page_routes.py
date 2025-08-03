from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def home():
    return render_template("register.html")

@page_bp.route("/login")
def login_page():
    return render_template("login.html")

@page_bp.route("/dashboard")
def dashboard():
    return render_template("index.html")
