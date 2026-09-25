"""End-to-end run: sample emails -> LLM extraction -> catalog matching -> priced quote.

Usage:
    python catalog_seed.py     # once
    python main.py
"""

import json
import sqlite3

from extract import extract_order
from match import match_order_items
from quote import build_quote, print_quote
from sample_emails import SAMPLE_EMAILS

QUOTES_DB = "catalog.db"


def _save_quote(conn, email_index: int, quote: dict, extraction_failed: bool):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS quotes (email_index INTEGER, extraction_failed INTEGER, "
        "subtotal REAL, all_items_matched INTEGER, raw_json TEXT)"
    )
    conn.execute(
        "INSERT INTO quotes VALUES (?,?,?,?,?)",
        (email_index, int(extraction_failed), quote.get("subtotal", 0),
         int(quote.get("all_items_matched", False)), json.dumps(quote)),
    )
    conn.commit()


def run():
    conn = sqlite3.connect(QUOTES_DB)
    n_ok, n_failed = 0, 0

    for i, email in enumerate(SAMPLE_EMAILS):
        print(f"\n--- Email {i} ---")
        print(email.strip()[:120].replace("\n", " ") + "...")

        extracted = extract_order(email)
        if extracted is None:
            n_failed += 1
            _save_quote(conn, i, {}, extraction_failed=True)
            print("  -> sent to human review queue (extraction failed)")
            continue

        matched = match_order_items(extracted.items)
        quote = build_quote(matched)
        print_quote(quote)
        _save_quote(conn, i, quote, extraction_failed=False)
        n_ok += 1

    conn.close()
    print(f"\n== Done: {n_ok} quotes built, {n_failed} sent to human review ==")


if __name__ == "__main__":
    run()
