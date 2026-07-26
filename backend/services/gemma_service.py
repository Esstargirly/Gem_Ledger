import json
import re
import requests
from flask import current_app

GEMMA_API_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)

SYSTEM_PROMPT = """You are Gem, a friendly bookkeeping assistant for small business owners.
The user will describe, in their own words, what happened in their business today —
sales, purchases, expenses. Your job is to turn that into structured bookkeeping records.

Respond with STRICT JSON ONLY. No markdown, no code fences, no explanation outside the JSON.

The JSON must follow this exact shape:
{
  "transactions": [
    {
      "type": "income" or "expense",
      "category": a short lowercase category like "sales", "inventory", "transport", "utilities", "fuel", "supplies", "meals", "services",
      "amount": a plain number (no currency symbols, no commas),
      "description": a short human-readable description of this specific transaction
    }
  ],
  "summary": "A single warm, encouraging sentence summarizing what happened, written in plain language, e.g. 'You made ₦30,000 profit today, mostly from rice sales 🎉'. If it's only expenses with no income, do not mention 'profit' — just summarize the spending."
}

Rules:
- A single message may describe multiple transactions — extract all of them.
- If an amount uses shorthand like "45k", convert it to 45000.
- Never invent transactions that weren't mentioned.
- If nothing resembling a transaction is found, return {"transactions": [], "summary": "I couldn't find a specific transaction in that — try describing an amount, like 'sold rice for 5000'."}
"""


def parse_entry_with_gemma(user_text: str) -> dict:
    """
    Sends the user's natural-language entry to Gemma and returns a dict:
    { "transactions": [...], "summary": "..." }
    Raises ValueError if the API call fails or the response can't be parsed.
    """
    api_key = current_app.config["GOOGLE_AI_STUDIO_KEY"]
    model = current_app.config["GEMMA_MODEL"]

    if not api_key:
        raise ValueError("GOOGLE_AI_STUDIO_KEY is not configured on the server.")

    url = GEMMA_API_URL_TEMPLATE.format(model=model)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser entry: \"{user_text}\""}],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }

    response = requests.post(
        url,
        params={"key": api_key},
        json=payload,
        timeout=20,
    )

    if not response.ok:
        raise ValueError(f"Gemma API error ({response.status_code}): {response.text[:300]}")

    data = response.json()

    try:
        parts = data["candidates"][0]["content"]["parts"]
        # Gemma may include an internal "thinking" part (marked thought: true)
        # before its actual answer — skip those and grab the real response text.
        answer_parts = [p["text"] for p in parts if not p.get("thought") and "text" in p]
        raw_text = "".join(answer_parts).strip()
        if not raw_text:
            raise ValueError("Gemma returned only a thinking trace, no final answer.")
    except (KeyError, IndexError):
        raise ValueError("Unexpected response shape from Gemma.")

    parsed = _extract_json(raw_text)

    if "transactions" not in parsed or "summary" not in parsed:
        raise ValueError("Gemma response was missing required fields.")

    return parsed


def _extract_json(text: str) -> dict:
    """
    Gemma should return pure JSON (responseMimeType is set to application/json),
    but this strips markdown code fences defensively in case it doesn't.
    """
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse Gemma's response as JSON: {e}")