"""Matches an extracted line item description against the product catalog.

Free, local, no embeddings API: rapidfuzz does string-similarity matching.
Anything below CONFIDENCE_THRESHOLD is flagged for human review instead of
being guessed at — this is the "fallback path for items the model can't
confidently match" the project is meant to demonstrate.
"""

import sqlite3

from rapidfuzz import fuzz, process

DB_PATH = "catalog.db"
CONFIDENCE_THRESHOLD = 70  # 0-100 rapidfuzz score


def _load_catalog(conn):
    rows = conn.execute("SELECT id, name, spec, unit_price FROM products").fetchall()
    return rows


def match_item(description: str, spec: str | None, catalog_rows) -> dict:
    query = f"{description} {spec or ''}".strip()
    names = [row[1] for row in catalog_rows]

    best = process.extractOne(query, names, scorer=fuzz.token_sort_ratio)
    if best is None:
        return {"matched": False, "reason": "no catalog candidates"}

    match_name, score, idx = best
    if score < CONFIDENCE_THRESHOLD:
        return {
            "matched": False,
            "reason": f"low confidence ({score:.0f} < {CONFIDENCE_THRESHOLD})",
            "closest_guess": match_name,
            "closest_score": score,
        }

    row = catalog_rows[idx]
    return {
        "matched": True,
        "product_id": row[0],
        "product_name": row[1],
        "unit_price": row[3],
        "confidence": score,
    }


def match_order_items(items, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    catalog_rows = _load_catalog(conn)
    conn.close()

    results = []
    for item in items:
        m = match_item(item.description, item.spec, catalog_rows)
        m["quantity"] = item.quantity
        m["description"] = item.description
        results.append(m)
    return results
