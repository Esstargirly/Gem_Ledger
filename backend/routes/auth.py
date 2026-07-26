from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
import jwt

from extensions import db, bcrypt
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _make_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=current_app.config["JWT_EXPIRY_DAYS"]),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    business_name = (data.get("business_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not business_name or not email or not password:
        return jsonify({"error": "Business name, email, and password are all required."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(business_name=business_name, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    token = _make_token(user.id)

    return jsonify({"token": token, "business_name": user.business_name}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect email or password."}), 401

    token = _make_token(user.id)

    return jsonify({"token": token, "business_name": user.business_name}), 200