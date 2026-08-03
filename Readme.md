# GemLedger

**Keep Your Books. Grow Your Business.**

GemLedger is an AI bookkeeping assistant built for small business owners who don’t have time (or training) for traditional accounting. You type or speak what happened in your business today — what you sold, what you bought — and [Gemma 4](https://ai.google.dev/gemma) turns it into structured financial records automatically.

Built for the Gemma 4 Hackathon.

Live app link: https://gem-ledger-frontend.onrender.com

## How to use the app

1. **Sign up** — go to the [live site](https://gem-ledger-frontend.onrender.com), click **Sign Up**, and enter your business name, email, and password.
2. **Log in** — use the same email and password to log in from then on.
3. **Add an entry** — on the Home page, type (or speak, in Chrome) what happened in your business
4. **Click Add Entry** — Gemma 4 reads it and splits it into structured records (income and expenses), and shows a quick summary.
5. **Check your Records page** — see every entry in a table, along with your total income, total expenses, and net profit.
6. **Export a PDF** — on the Records page, click Export to download your records as a PDF you can share with a bank, cooperative, or accountant.
7. **Manage your account** — visit Settings to see your business name and email, or log out.

## How Gemma 4 is used

## Why this project matters

Most small business owners — market traders, shop owners, roadside vendors — don’t keep formal books. Not because they don’t care about their money, but because traditional bookkeeping (spreadsheets, accounting software, ledgers) takes time and training they don’t have. So sales and expenses end up scattered across memory, notebooks, or nowhere at all.

That has real consequences:

- **No way to know if the business is actually profitable** — money moves in and out, but no one’s tracking the net
- **No records to show a bank or lender** when applying for credit to grow the business
- **No paper trail** for tax purposes or resolving disputes with suppliers/customers

GemLedger closes that gap by making bookkeeping as easy as talking. There’s no learning curve, no manual data entry, no spreadsheet formulas — just plain language in, structured financial records out. That’s what makes it a strong fit for the problem: it meets business owners at the effort level they’re already working at, instead of asking them to adopt a new skill.

**Key benefits:**

- **Zero learning curve** — if you can describe your sales in a sentence, you can use GemLedger
- **Works by voice or text**, so it’s usable even for owners less comfortable typing
- **Automatic categorization**, so records stay organized without manual tagging
- **Real-time income, expense, and profit totals** — instant financial visibility instead of doing the math yourself
- **Exportable PDF records** — a ready-made document for a bank, cooperative, or accountant
- **Fast to adopt** — built and deployed as a full working product in a single day, showing it’s lightweight enough to actually get used, not just demoed

## What it does

- **Type or speak a plain-language entry**, like: *“Sold 5 bags of rice for 25,000, paid 5,000 for transport”*
- **Gemma 4 parses it** into structured transactions — type (income/expense), category, amount, description
- **See your income, expenses, and net profit** update automatically
- **Voice input** using the browser’s built-in speech recognition — no separate transcription service needed
- **Export your records as a PDF** to share with a bank, co-op, or accountant

## How Gemma 4 is used

The core of GemLedger is a single prompt sent to Gemma 4 (`gemma-4-26b-a4b-it`) via the Google AI Studio API. It’s instructed to:

1. Return strict JSON only, matching a fixed schema
1. Infer a category for each transaction on its own
1. Understand shorthand numbers (e.g. “45k” → 45000)
1. Extract multiple transactions from a single message
1. Write a short, friendly summary sentence

See [`backend/services/gemma_service.py`](backend/services/gemma_service.py) for the full prompt and parsing logic.

## Tech stack

|Layer     |Tech                                                    |
|----------|--------------------------------------------------------|
|Frontend  |Tailwind CSS + vanilla JavaScript (no build step)       |
|Backend   |Flask (Python)                                          |
|Database  |PostgreSQL (hosted on Neon)                             |
|AI Model  |Gemma 4 via Google AI Studio                            |
|Auth      |JWT (bcrypt-hashed passwords)                           |
|PDF Export|jsPDF (client-side, no backend needed)                  |
|Hosting   |Render (backend as Web Service, frontend as Static Site)|

## Project structure

```
gemledger/
├── backend/
│   ├── app.py                    # Flask entry point
│   ├── config.py                 # Environment config, DB connection settings
│   ├── extensions.py             # db, bcrypt initialization
│   ├── models.py                 # User and Transaction models
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── auth.py               # /auth/signup, /auth/login
│   │   └── transactions.py       # /analyze, /transactions
│   ├── services/
│   │   └── gemma_service.py      # Gemma 4 prompt + parsing logic
│   └── utils/
│       └── auth_middleware.py    # JWT auth decorator
│
└── frontend/
    ├── index.html                # Landing page
    ├── signup.html
    ├── login.html
    ├── home.html                 # Entry screen (text/voice input)
    ├── records.html              # Transaction table + PDF export
    ├── settings.html              # Account info + logout
    └── js/
        ├── api.js                # Shared fetch helper (JWT handling)
        ├── auth.js                # Signup/login logic
        ├── entry.js               # Text/voice entry + Gemma call
        ├── records.js             # Transaction table rendering + PDF export
        └── settings.js            # Settings page logic


## License

Built for the Gemma 4 Hackathon, 2026.



