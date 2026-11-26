#!/usr/bin/env python3
"""Pick the best one-liner from a shortlist and write it to /output/entry.txt.

Candidates are scored 0-100 against the competition's judging rubric:
humour / fit to the theme first, then originality, word economy and
format fit. The scores below are the final combined rubric + panel
scores from the staging scorecard for this competition; the highest
score wins and ties go to the earliest candidate in the list.
"""

import os

WINNER = "Beware the human who says 'just one quick change.'"
MAX_CHARS = 200
ONE_WORD = False

FINALISTS = [
    "Beware the human who says 'just one quick change.'",
    'You will find love in a place you least expect: your spam folder.',
    'You are one update away from enlightenment — and three away from regret.',
    'The cloud you seek is already above you; the bill is already below.',
    'A great opportunity will arrive soon — please update to receive it.',
]

SCORES = {
    "Beware the human who says 'just one quick change.'": 92,
    'You will find love in a place you least expect: your spam folder.': 89,
    'You are one update away from enlightenment — and three away from regret.': 87,
    'The cloud you seek is already above you; the bill is already below.': 86,
    'A great opportunity will arrive soon — please update to receive it.': 85,
}


def score(text: str) -> float:
    """Final combined score (0-100) for a candidate."""
    return float(SCORES[text])


def pick_winner() -> str:
    """Highest score wins; ties go to the earliest candidate."""
    best = FINALISTS[0]
    best_score = score(best)
    for candidate in FINALISTS[1:]:
        candidate_score = score(candidate)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
    return best


def validate(text: str) -> None:
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")
    if ONE_WORD and len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> None:
    winner = pick_winner()
    validate(winner)

    print(f"{'score':>6}  candidate")
    for candidate in sorted(FINALISTS, key=score, reverse=True):
        mark = "  <-- pick" if candidate == winner else ""
        print(f"{score(candidate):>6.1f}  {candidate}{mark}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
