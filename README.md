# Order-email-to-quote pipeline

Free-text order email → validated structured line items (LLM) → matched
against a product catalog (fuzzy match) → priced quote, with unmatched items
routed to a "needs review" list instead of being guessed at.

Maps to Unilog's own example: *"an emailed order becomes a priced quote."*

## Run it — step by step

1. **Install Ollama** (free) and pull a small model (one-time, ~2 GB):
   ```bash
   ollama pull llama3.2
   ollama serve   # leave running in its own terminal
   ```

2. **Set up Python:**
   ```bash
   cd order_email_to_quote
   python3 -m venv .venv
   source .venv/bin/activate       # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Build the synthetic catalog** (5,000 products, SQLite, free):
   ```bash
   python catalog_seed.py
   ```
   You should see `Seeded 5000 products into catalog.db`.

4. **Run the pipeline** over the sample emails:
   ```bash
   python main.py
   ```
   For each of the 10 sample emails you'll see: the email, each matched line
   item with its price, a subtotal, and any items that couldn't be confidently
   matched (flagged for human review, not guessed).

5. **(Optional) Run the mini eval harness:**
   ```bash
   python eval.py
   ```
   Scores extraction accuracy against a small hand-labeled set — this is the
   piece to point to when asked "how do you measure quality?"

## What to say about it in the interview

- **Schema validation + fallback:** `extract.py` validates the model's JSON
  against a Pydantic schema and retries once with the validation error fed
  back in; `main.py` routes a still-failing email to a review queue instead
  of crashing or guessing.
- **Ranking vs. data problem:** `match.py`'s `CONFIDENCE_THRESHOLD` is exactly
  the knob the JD mentions — below it, the item goes to `needs_review` rather
  than being silently mismatched.
- **Own a number:** `eval.py` is a first pass at "prove it worked" — in a real
  system this would be a larger golden set with per-field accuracy, logged
  over time.
- **Where you'd take it next:** swap SQLite for Postgres, rapidfuzz for a
  hybrid lexical+embedding search, and add persisted logging of every
  extraction/match/price decision for observability.
