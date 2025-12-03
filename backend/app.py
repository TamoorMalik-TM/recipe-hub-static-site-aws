
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from db import init_db, get_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

init_db()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user_id = data["user_id"]
        except Exception:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user_id, *args, **kwargs)
    return decorated


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/auth/register", methods=["POST"])
def register():
    payload = request.get_json() or {}
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        return jsonify({"message": "username already exists"}), 400

    hashed = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, "user"),
    )
    db.commit()
    return jsonify({"message": "user created"}), 201


@app.route("/auth/login", methods=["POST"])
def login():
    payload = request.get_json() or {}
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, password_hash, role FROM users WHERE username = ?", (username,)
    )
    row = cur.fetchone()
    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"message": "invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": row["id"],
            "role": row["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token}), 200


@app.route("/recipes", methods=["GET"])
def list_recipes():
    tag = request.args.get("tag")
    search = request.args.get("search")

    db = get_db()
    cur = db.cursor()

    query = "SELECT r.id, r.title, r.description, r.tags, r.difficulty, r.prep_time, r.cook_time, r.image_url, u.username AS author FROM recipes r JOIN users u ON r.user_id = u.id"
    clauses = []
    params = []

    if tag:
        clauses.append("r.tags LIKE ?")
        params.append(f"%{tag}%")
    if search:
        clauses.append("(r.title LIKE ? OR r.description LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY r.created_at DESC"
    cur.execute(query, params)
    rows = cur.fetchall()

    recipes = []
    for row in rows:
        recipes.append(
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "tags": row["tags"],
                "difficulty": row["difficulty"],
                "prep_time": row["prep_time"],
                "cook_time": row["cook_time"],
                "image_url": row["image_url"],
                "author": row["author"],
            }
        )

    return jsonify(recipes), 200


@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT r.*, u.username AS author FROM recipes r JOIN users u ON r.user_id = u.id WHERE r.id = ?",
        (recipe_id,),
    )
    row = cur.fetchone()
    if not row:
        return jsonify({"message": "recipe not found"}), 404

    cur.execute(
        "SELECT AVG(rating) AS avg_rating, COUNT(*) AS votes FROM ratings WHERE recipe_id = ?",
        (recipe_id,),
    )
    rating_row = cur.fetchone()
    avg_rating = rating_row["avg_rating"] if rating_row["avg_rating"] is not None else 0
    votes = rating_row["votes"]

    recipe = {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "ingredients": row["ingredients"],
        "steps": row["steps"],
        "tags": row["tags"],
        "difficulty": row["difficulty"],
        "prep_time": row["prep_time"],
        "cook_time": row["cook_time"],
        "servings": row["servings"],
        "image_url": row["image_url"],
        "author": row["author"],
        "avg_rating": avg_rating,
        "votes": votes,
    }
    return jsonify(recipe), 200


@app.route("/recipes", methods=["POST"])
@token_required
def create_recipe(current_user_id):
    payload = request.get_json() or {}

    required_fields = ["title", "description", "ingredients", "steps"]
    if not all(payload.get(f) for f in required_fields):
        return jsonify({"message": "missing required fields"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO recipes
        (user_id, title, description, ingredients, steps, tags, difficulty, prep_time,
         cook_time, servings, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            current_user_id,
            payload.get("title"),
            payload.get("description"),
            payload.get("ingredients"),
            payload.get("steps"),
            payload.get("tags", ""),
            payload.get("difficulty", "medium"),
            payload.get("prep_time", 0),
            payload.get("cook_time", 0),
            payload.get("servings", 1),
            payload.get("image_url", ""),
            datetime.datetime.utcnow().isoformat(),
        ),
    )
    db.commit()
    recipe_id = cur.lastrowid
    return jsonify({"id": recipe_id, "message": "recipe created"}), 201


@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
@token_required
def update_recipe(current_user_id, recipe_id):
    payload = request.get_json() or {}
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    )
    row = cur.fetchone()
    if not row:
        return jsonify({"message": "recipe not found"}), 404

    if row["user_id"] != current_user_id:
        return jsonify({"message": "not allowed"}), 403

    fields = [
        "title",
        "description",
        "ingredients",
        "steps",
        "tags",
        "difficulty",
        "prep_time",
        "cook_time",
        "servings",
        "image_url",
    ]
    updates = []
    params = []
    for f in fields:
        if f in payload:
            updates.append(f"{f} = ?")
            params.append(payload[f])

    if not updates:
        return jsonify({"message": "nothing to update"}), 400

    params.append(recipe_id)
    cur.execute(
        f"UPDATE recipes SET {', '.join(updates)} WHERE id = ?",
        params,
    )
    db.commit()
    return jsonify({"message": "recipe updated"}), 200


@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@token_required
def delete_recipe(current_user_id, recipe_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT user_id FROM recipes WHERE id = ?", (recipe_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"message": "recipe not found"}), 404

    if row["user_id"] != current_user_id:
        return jsonify({"message": "not allowed"}), 403

    cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
    return jsonify({"message": "recipe deleted"}), 200


@app.route("/recipes/<int:recipe_id>/rate", methods=["POST"])
@token_required
def rate_recipe(current_user_id, recipe_id):
    payload = request.get_json() or {}
    rating = payload.get("rating")
    if rating is None or not (1 <= int(rating) <= 5):
        return jsonify({"message": "rating must be between 1 and 5"}), 400

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,))
    if not cur.fetchone():
        return jsonify({"message": "recipe not found"}), 404

    cur.execute(
        "INSERT INTO ratings (user_id, recipe_id, rating) VALUES (?, ?, ?)",
        (current_user_id, recipe_id, int(rating)),
    )
    db.commit()
    return jsonify({"message": "rating saved"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
