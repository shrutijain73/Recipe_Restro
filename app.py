import prompt
from agent import agent
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import markdown
from dotenv import load_dotenv


import tool

from test import mail

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change-me")  # set FLASK_SECRET in .env in production


DB_PATH = "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

def create_user(username, email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        # Update the SQL to include the email column
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return check_password_hash(row[0], password)
def get_user_email(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
# Initialize DB at startup
init_db()

# --- Routes ---
@app.route("/")
def home():
    # Public descriptive landing page. If logged in, redirect to dashboard.
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for("signup"))
        ok = create_user(username, email, password)
        if ok:
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists", "danger")
            return redirect(url_for("signup"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if authenticate_user(username, password):
            session["username"] = username
            session["email"] = get_user_email(username)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out", "info")
    return redirect(url_for("home"))

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

# --- Dashboard / Menu ---
@app.route("/dashboard")
@login_required
def dashboard():
    # Render the options menu (choose.html)
    return render_template("choose.html", username=session.get("username"))

# Individual option pages (one page per option)
@app.route("/choose")
@login_required
def choose():
    return render_template("choose.html", username=session.get("username"))

@app.route("/choose/protein")
@login_required
def choose_protein():
    return render_template("choose_protein.html", username=session.get("username"))

@app.route("/choose/energy")
@login_required
def choose_energy():
    return render_template("choose_energy.html", username=session.get("username"))

@app.route("/choose/carbs")
@login_required
def choose_carbs():
    return render_template("choose_carbs.html", username=session.get("username"))

@app.route("/choose/region")
@login_required
def choose_region():
    return render_template("choose_region.html", username=session.get("username"))

@app.route("/choose/include-exclude")
@login_required
def choose_include_exclude():
    return render_template("choose_include_exclude.html", username=session.get("username"))

@app.route("/choose/title")
@login_required
def choose_recipe_title():
    return render_template("choose_recipe_title.html", username=session.get("username"))

# --- API endpoints that wrap your tool functions ---
# (no changes to the API endpoints you already have)
@app.route("/api/protein", methods=["POST"])
@login_required
def api_protein():
    data = request.json or {}
    # Retrieve the logged-in user's email (username)
    user_email = session.get("email") 
    
    user_query = f"Give a high protein dish with protein range min: {data.get('min_protein')}, max: {data.get('max_protein')}."
    try:
        # Pass the email to the agent for automatic mailing
        result = agent(prompt.protein_prompt, user_query)

        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/energy", methods=["POST"])
@login_required
def api_energy():
    data = request.json or {}
    user_email = session.get("email")
    
    user_query = f"Give a high energy dish with energy range min: {data.get('min_energy')}, max: {data.get('max_energy')}."
    try:
        result = agent(prompt.Energy_prompt, user_query)
        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/carbs", methods=["POST"])
@login_required
def api_carbs():
    data = request.json or {}
    user_email = session.get("email")
    
    user_query = f"Give a high carbs dish with carbs range min: {data.get('min_carbs')}, max: {data.get('max_carbs')}."
    try:
        result = agent(prompt.Carbs_prompt, user_query)
        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/region", methods=["POST"])
@login_required
def api_region():
    data = request.json or {}
    user_email = session.get("email")
    region = data.get("region", "")
    diet = data.get("diet", "")
    user_query = f"Give a best in nutrition dish with region name: {region}, diet type: {diet}."
    try:
        result = agent(prompt.diet_by_region_prompt, user_query)
        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/title", methods=["POST"])
@login_required
def api_title():
    data = request.json or {}
    user_email = session.get("email")
    title = data.get("title", "")
    user_query = f"Give a recipe instruction and ingredient information with recipe name: {title}."
    try:
        result = agent(prompt.recipe_with_title_prompt, user_query)
        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    

@app.route("/api/meal-plan", methods=["POST"])
@login_required
def api_meal_plan():
    data = request.json or {}
    user_email = session.get("email")
    calories = data.get("calories_per_day", 2000)
    days = data.get("days", 1)
    
    user_query = f"Give a file for meal plane as pdf including(Breakfast, Lunch, dinner) with calories per day: {calories}, days: {days}."
    try:
        raw_result = agent(prompt.meal_plane_prompt, user_query)

        mailVar = mail(raw_result, user_email, files=True)
        return jsonify({"ok": True, "result": markdown.markdown(mailVar)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/include-exclude", methods=["POST"])
@login_required
def api_include_exclude():
    data = request.json or {}
    user_email = session.get("email") # Automatically get the logged-in user's email
    
    includeIngredients = data.get("includeIngredients", "")
    excludeIngredients = data.get("excludeIngredients", "")
    includeCategories = data.get("includeCategories", "")
    excludeCategories = data.get("excludeCategories", "")
    page = int(data.get("page", 1))
    title = data.get("title", "")
    
    # Construct a detailed query for the Agent
    user_query = (f"Give a recipe with name: {title}. "
                  f"Include: {includeIngredients}, Exclude: {excludeIngredients}. "
                  f"Categories to include: {includeCategories}, exclude: {excludeCategories}. "
                  f"Check page: {page}.")
    
    try:
        # The agent now handles the logic, PDF creation, and Email delivery
        result = agent(prompt.including_and_excluding_ingredients_categories_and_title_prompt, 
                       user_query)
        
        mailVar = mail(result, user_email)
        return jsonify({"ok": True, "result": mailVar})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/recipe-instruction", methods=["POST"])
@login_required
def api_recipe_instruction():
    data = request.json or {}
    recipe_id = int(data.get("recipe_id", 0))
    try:
        result = tool.recipe_instruction(recipe_id)
        return jsonify({"ok": True, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/ingredients", methods=["POST"])
@login_required
def api_ingredients():
    data = request.json or {}
    recipe_id = int(data.get("recipe_id", 0))
    try:
        result = tool.ingrendints(recipe_id)
        return jsonify({"ok": True, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

