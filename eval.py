"""A tiny evaluation harness — the piece the JD calls out as easy to skip.

Hand-labels the expected item count for a handful of emails and checks the
LLM's extraction against it. In a real system this would be a persisted
golden set with per-field accuracy, not just item counts — this is a
deliberately minimal version to demonstrate the idea in an interview.
"""

from extract import extract_order

GOLDEN_SET = [
    ("""order: 10x 1/2" copper elbow, 4 ea 3/4 in PVC coupling, two circuit breakers""", 3),
    ("""need copper tee x6 (3/4") and 2 junction boxes""", 2),
    ("""quick order — 6x brass adapter half inch, and one refrigerant line""", 2),
]


def run_eval():
    correct = 0
    for email, expected_count in GOLDEN_SET:
        result = extract_order(email)
        actual_count = len(result.items) if result else 0
        ok = actual_count == expected_count
        correct += ok
        print(f"expected {expected_count} items, got {actual_count} -> {'OK' if ok else 'MISS'}")

    accuracy = correct / len(GOLDEN_SET)
    print(f"\nItem-count accuracy: {accuracy:.0%} ({correct}/{len(GOLDEN_SET)})")


if __name__ == "__main__":
    run_eval()
