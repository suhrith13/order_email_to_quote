"""Generates a synthetic HVAC/plumbing/electrical product catalog into SQLite.

Free and local: no download, no external dataset. Run once:
    python catalog_seed.py
"""

import random
import sqlite3

DB_PATH = "catalog.db"

MATERIALS = ["Copper", "PVC", "Brass", "Steel", "Galvanized", "PEX"]
FITTINGS = ["Elbow", "Coupling", "Tee", "Valve", "Union", "Adapter", "Cap", "Reducer"]
SIZES = ['1/4"', '1/2"', '3/4"', '1"', '1.25"', '1.5"', '2"']
ELECTRICAL = ["Circuit Breaker", "Outlet", "Switch", "Wire Nut", "Conduit", "Junction Box"]
HVAC = ["Duct Elbow", "Filter", "Thermostat", "Blower Motor", "Refrigerant Line", "Vent Grille"]

random.seed(42)


def build_catalog(n_rows: int = 5000):
    rows = []
    pid = 1
    categories = [
        ("plumbing", MATERIALS, FITTINGS, SIZES),
        ("electrical", [None], ELECTRICAL, [None]),
        ("hvac", [None], HVAC, [None]),
    ]
    while len(rows) < n_rows:
        cat_name, materials, items, sizes = random.choice(categories)
        material = random.choice(materials)
        item = random.choice(items)
        size = random.choice(sizes)
        name_parts = [p for p in [size, material, item] if p]
        name = " ".join(name_parts)
        spec = f"{material or ''} {size or ''}".strip() or None
        price = round(random.uniform(0.75, 240.0), 2)
        rows.append((pid, name, cat_name, spec, price))
        pid += 1
    return rows


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute(
        """CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            spec TEXT,
            unit_price REAL NOT NULL
        )"""
    )
    rows = build_catalog(5000)
    conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", rows)
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    print(f"Seeded {count} products into {DB_PATH}")
    for row in conn.execute("SELECT * FROM products LIMIT 5"):
        print(" example:", row)
    conn.close()


if __name__ == "__main__":
    main()
