"""Builds a priced quote from matched line items, splitting out unmatched ones."""


def build_quote(matched_results: list[dict]) -> dict:
    priced = [r for r in matched_results if r["matched"]]
    needs_review = [r for r in matched_results if not r["matched"]]

    for r in priced:
        r["line_total"] = round(r["unit_price"] * r["quantity"], 2)

    subtotal = round(sum(r["line_total"] for r in priced), 2)

    return {
        "priced_items": priced,
        "needs_review": needs_review,
        "subtotal": subtotal,
        "all_items_matched": len(needs_review) == 0,
    }


def print_quote(quote: dict) -> None:
    print("  Priced items:")
    for r in quote["priced_items"]:
        print(f"    {r['quantity']:>3} x {r['product_name']:<40} "
              f"@ ${r['unit_price']:>7.2f}  = ${r['line_total']:>8.2f}  "
              f"(match confidence {r['confidence']:.0f})")
    print(f"  Subtotal: ${quote['subtotal']:.2f}")

    if quote["needs_review"]:
        print("  NEEDS HUMAN REVIEW (could not confidently match):")
        for r in quote["needs_review"]:
            guess = r.get("closest_guess", "n/a")
            print(f"    {r['quantity']:>3} x '{r['description']}' -> closest guess: {guess} ({r['reason']})")
