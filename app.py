"""
Online Plant Nursery - Flask Backend
"""

import os
import sqlite3
import re
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, g
)
from werkzeug.security import generate_password_hash, check_password_hash

def create_table():
    conn = sqlite3.connect("plants.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-change-me")
DATABASE = os.path.join(os.path.dirname(__file__), "plants.db")

PLANTS = [
    {"id": 1,  "name": "Money Plant",       "category": "Indoor",    "price": 199, "image": "static/money plant.jpeg",              "description": "Easy-care vining plant believed to bring prosperity. Thrives in low light."},
    {"id": 2,  "name": "Snake Plant",       "category": "Indoor",    "price": 349, "image": "static/snake-plant.webp",     "description": "Hardy air-purifier that tolerates neglect and low light beautifully."},
    {"id": 3,  "name": "Peace Lily",        "category": "Indoor",    "price": 449, "image": "static/peace lily.jpeg",         "description": "Elegant white blooms and lush green leaves. Loves shaded corners."},
    {"id": 4,  "name": "Areca Palm",        "category": "Indoor",    "price": 599, "image": "static/areca palm.webp",       "description": "Feathery fronds add a tropical vibe to any living space."},
    {"id": 5,  "name": "Rose Plant",        "category": "Outdoor",   "price": 299, "image": "https://loremflickr.com/800/600/rose,flower,red?lock=105",           "description": "Classic fragrant rose that blooms through most of the year."},
    {"id": 6,  "name": "Hibiscus",          "category": "Outdoor",   "price": 249, "image": "https://loremflickr.com/800/600/hibiscus,flower?lock=106",           "description": "Vivid trumpet-shaped flowers, perfect for Indian gardens and balconies."},
    {"id": 7,  "name": "Jasmine (Mogra)",   "category": "Outdoor",   "price": 279, "image": "static/jasmine.webp",      "description": "Sweetly scented white flowers that bloom through summer evenings."},
    {"id": 8,  "name": "Bougainvillea",     "category": "Outdoor",   "price": 399, "image": "https://loremflickr.com/800/600/bougainvillea,purple,flower?lock=108","description": "Cascading magenta blooms — a sun-loving showstopper."},
    {"id": 9,  "name": "Tulsi (Holy Basil)","category": "Medicinal", "price": 149, "image": "static/Tulasi.jpeg",          "description": "Sacred Indian herb known for its immunity-boosting properties."},
    {"id": 10, "name": "Aloe Vera",         "category": "Medicinal", "price": 199, "image": "static/Aloevera.webp",      "description": "Soothing succulent for skin care and digestion. Loves bright sun."},
    {"id": 11, "name": "Neem Plant",        "category": "Medicinal", "price": 329, "image": "static/Neem.jpeg",         "description": "Ayurvedic powerhouse used for skin, hair and natural pest control."},
    {"id": 12, "name": "Mint (Pudina)",     "category": "Medicinal", "price": 129, "image": "static/mint.jpeg",           "description": "Aromatic culinary herb that aids digestion and freshens breath."},
    {"id": 13, "name": "Spider Plant", "category": "Indoor", "price": 259, "image": "static/spider plant.jpeg", "description": "Fast-growing indoor plant with arching leaves, great for beginners and air purification."},
    {"id": 14, "name": "ZZ Plant", "category": "Indoor", "price": 499, "image": "static/zz plant.jpeg", "description": "Glossy, drought-tolerant plant that thrives even in very low light conditions."},
    {"id": 15, "name": "Rubber Plant", "category": "Indoor", "price": 399, "image": "static/rubber plant.jpeg", "description": "Stylish indoor plant with large dark green leaves, perfect for modern interiors."},
    {"id": 16, "name": "Marigold", "category": "Outdoor", "price": 149, "image": "static/marygold.jpeg", "description": "Bright orange and yellow flowers widely used in Indian festivals and gardens."},
    {"id": 17, "name": "Sunflower", "category": "Outdoor", "price": 199, "image": "static/sunflower.jpeg", "description": "Tall plant with large yellow blooms that follow the sun, adding vibrancy outdoors."},
    {"id": 18, "name": "Chrysanthemum", "category": "Outdoor", "price": 229, "image": "static/Chrysanthemum.jpeg", "description": "Colorful seasonal flowers that bloom in winter and brighten up gardens."},
    {"id": 19, "name": "Ashwagandha", "category": "Medicinal", "price": 199, "image": "static/ashwagandha.jpeg", "description": "Ancient medicinal herb known for reducing stress and improving vitality."},
    {"id": 20, "name": "Lemongrass", "category": "Medicinal", "price": 179, "image": "static/lemon grass.jpeg", "description": "Citrusy herb used in teas and cooking, known for digestive and calming benefits."},
    {"id": 21, "name": "Curry Leaves Plant", "category": "Medicinal", "price": 249, "image": "static/curry leaves.jpeg", "description": "Essential Indian herb used in cooking, rich in nutrients and medicinal properties."},
    {"id": 22, "name": "Boston Fern", "category": "Indoor", "price": 299, "image": "static/boston fern.jpeg", "description": "Lush green fern that thrives in humidity and adds freshness to indoor spaces."},
    {"id": 23, "name": "Calathea", "category": "Indoor", "price": 449, "image": "static/calathea.jpeg", "description": "Decorative plant with patterned leaves that move with light changes."},
    {"id": 24, "name": "Anthurium", "category": "Indoor", "price": 499, "image": "static/calathea.jpeg", "description": "Bright red heart-shaped flowers that bring color to indoor decor."},
    {"id": 25, "name": "Petunia", "category": "Outdoor", "price": 179, "image": "static/petunia.jpeg", "description": "Colorful and easy-to-grow flowering plant perfect for balconies and gardens."},
    {"id": 26, "name": "Lavender", "category": "Outdoor", "price": 299, "image": "static/lavender.jpeg", "description": "Fragrant purple flowers known for calming aroma and ornamental beauty."},
    {"id": 27, "name": "Ixora", "category": "Outdoor", "price": 249, "image": "static/ixora.jpeg", "description": "Clustered bright flowers commonly found in tropical gardens."},
    {"id": 28, "name": "Giloy (Guduchi)", "category": "Medicinal", "price": 199, "image": "static/giloy.jpeg", "description": "Ayurvedic climber known for boosting immunity and detoxifying the body."},
    {"id": 29, "name": "Brahmi", "category": "Medicinal", "price": 159, "image": "static/bramhi.jpeg", "description": "Herb used to improve memory, focus, and brain health."},
    {"id": 30, "name": "Stevia Plant", "category": "Medicinal", "price": 189, "image": "static/stevia.jpeg", "description": "Natural sweetener plant used as a sugar substitute, ideal for diabetics."}
]

CATEGORIES = ["Indoor", "Outdoor", "Medicinal"]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.context_processor
def inject_globals():
    cart = session.get("cart", {})
    return {
        "current_user": session.get("username"),
        "cart_count": sum(cart.values()),
        "categories": CATEGORIES,
    }

def find_plant(plant_id):
    return next((p for p in PLANTS if p["id"] == plant_id), None)

@app.route("/")
def home():
    return render_template("index.html", featured=PLANTS[:6])

@app.route("/plants")
def plants():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    results = PLANTS
    if category and category in CATEGORIES:
        results = [p for p in results if p["category"] == category]
    if query:
        results = [p for p in results if query in p["name"].lower() or query in p["description"].lower()]
    return render_template("plants.html", plants=results, query=query, active_category=category)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        conn = sqlite3.connect("plants.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        flash("Message sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("signup.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Please enter a valid email address.", "error")
            return render_template("signup.html")
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, generate_password_hash(password)))
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
            return render_template("signup.html")
        session["username"] = username
        flash(f"Welcome to Greenleaf, {username}!", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE lower(username) = ? OR lower(email) = ?",
                          (identifier, identifier)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials. Please try again.", "error")
        return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You've been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    cart_dict = session.get("cart", {})
    items = []
    total = 0
    for plant_id, qty in cart_dict.items():
        plant = find_plant(int(plant_id))
        if plant:
            line_total = plant["price"] * qty
            items.append({"plant": plant, "qty": qty, "line_total": line_total})
            total += line_total
    return render_template("cart.html", items=items, total=total)

@app.route("/cart/add/<int:plant_id>", methods=["POST"])
def add_to_cart(plant_id):
    plant = find_plant(plant_id)
    if not plant:
        return jsonify({"ok": False, "message": "Plant not found"}), 404
    cart = session.get("cart", {})
    key = str(plant_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return jsonify({"ok": True, "message": f"{plant['name']} added to cart", "cart_count": sum(cart.values())})

@app.route("/cart/update/<int:plant_id>", methods=["POST"])
def update_cart(plant_id):
    action = request.form.get("action", "remove")
    cart = session.get("cart", {})
    key = str(plant_id)
    if action == "increase":
        cart[key] = cart.get(key, 0) + 1
    elif action == "decrease":
        cart[key] = cart.get(key, 0) - 1
        if cart[key] <= 0:
            cart.pop(key, None)
    elif action == "remove":
        cart.pop(key, None)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart/checkout", methods=["POST"])
def checkout():
    if not session.get("username"):
        flash("Please log in to checkout.", "error")
        return redirect(url_for("login"))
    session["cart"] = {}
    flash("Order placed successfully! Your plants are on their way.", "success")
    return redirect(url_for("home"))

CHATBOT_RULES = [
    (["water", "watering", "thirsty"],   "Most indoor plants like a deep watering only when the top 2cm of soil feels dry. Outdoor plants in summer often need daily watering — early morning is best."),
    (["light", "sun", "sunlight"],       "Indoor plants like Money Plant and Snake Plant tolerate low light. Outdoor flowering plants like Rose, Hibiscus and Bougainvillea need 5-6 hours of direct sun."),
    (["fertilizer", "feed", "nutrient"], "Use a balanced NPK 19:19:19 fertilizer every 2-3 weeks during the growing season. Organic options like vermicompost work wonderfully too."),
    (["pest", "bug", "insect", "aphid"], "Try a neem oil spray (5ml in 1L water + a drop of soap) once a week. It's safe, organic and handles most common pests."),
    (["yellow", "yellowing"],            "Yellow leaves usually mean overwatering. Let the soil dry out and check that the pot has good drainage."),
    (["repot", "pot", "repotting"],      "Repot every 1-2 years using a pot one size larger. The best time is just before the growing season (Feb-March in India)."),
    (["tulsi", "basil"],                 "Tulsi loves full sun and well-drained soil. Pinch the flower buds to encourage bushier leaf growth."),
    (["aloe", "aloevera"],               "Aloe Vera prefers bright sun and very little water — let the soil dry completely between waterings to avoid root rot."),
    (["rose"],                           "Roses love morning sun. Prune in winter, water at the base (not on leaves), and feed with mustard cake every 3 weeks."),
    (["indoor"],                         "Great low-maintenance indoor picks: Money Plant, Snake Plant, Peace Lily, Areca Palm. They purify air and tolerate Indian indoor conditions."),
    (["medicinal"],                      "Top medicinal plants for Indian homes: Tulsi, Aloe Vera, Neem and Mint. Each offers unique health benefits and is easy to grow."),
    (["hello", "hi", "hey", "namaste"], "Namaste! I'm your plant-care assistant. Ask me about watering, sunlight, pests, fertilizer or any specific plant."),
    (["thanks", "thank"],               "Happy to help! May your plants thrive."),
]

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").lower().strip()
    if not message:
        return jsonify({"reply": "Ask me anything about plant care!"})
    for keywords, reply in CHATBOT_RULES:
        if any(k in message for k in keywords):
            return jsonify({"reply": reply})
    return jsonify({"reply": "I'm still learning! Try asking about watering, sunlight, fertilizer, pests, or specific plants like Tulsi, Aloe Vera or Rose."})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)