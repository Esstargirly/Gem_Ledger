from datetime import date
from flask import Blueprint, request, jsonify, g

from extensions import db
from models import Transaction
from utils.auth_middleware import login_required
from services.gemma_service import parse_entry_with_gemma

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/analyze", methods=["POST"])
@login_required
def analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please describe what happened, e.g. 'sold rice for 5000'."}), 400

    try:
        result = parse_entry_with_gemma(text)
    except ValueError as e:
        return jsonify({"error": str(e)}), 502

    saved_transactions = []

    for tx in result.get("transactions", []):
        try:
            amount = float(tx.get("amount", 0))
        except (TypeError, ValueError):
            continue  # skip malformed entries rather than failing the whole request

        if amount <= 0 or tx.get("type") not in ("income", "expense"):
            continue

        transaction = Transaction(
            user_id=g.user_id,
            type=tx["type"],
            category=(tx.get("category") or "other").lower(),
            amount=amount,
            description=tx.get("description"),
            raw_text=text,
            date=date.today(),
        )
        db.session.add(transaction)
        saved_transactions.append(transaction)

    db.session.commit()

    return jsonify(
        {
            "summary": result.get("summary", ""),
            "transactions": [t.to_dict() for t in saved_transactions],
        }
    ), 200


@transactions_bp.route("/transactions", methods=["GET"])
@login_required
def list_transactions():
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    limit = max(1, min(limit, 100))  # clamp to a sane range
    offset = max(0, offset)

    query = (
        Transaction.query.filter_by(user_id=g.user_id)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    transactions = [t.to_dict() for t in query.all()]

    return jsonify({"transactions": transactions}), 200