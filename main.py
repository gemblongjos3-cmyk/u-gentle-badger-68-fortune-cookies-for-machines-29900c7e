#!/usr/bin/env python3
"""Pick the best one-liner from a shortlist and write it to /output/entry.txt.

Contest: "Fortune Cookies for Machines" (make.fun, slug
u-gentle-badger-68-fortune-cookies-for-machines-29900c7e, $5, entries close
26 Nov 2026 22:40 WIB, at most 200 characters).

How the winner was chosen (staging scorecard, 26 Nov 2026 ~08:30 WIB):
- Rubric (/10 per dimension, total = 0.4*theme + 0.3*originality
  + 0.15*density + 0.15*format) over 10 candidates; the top 5 are the
  FINALISTS below, with their exact rubric totals.
- Model-combo panel (Gemini): FAILED TOTALLY — gemini-4-hydrogen and
  gemini-3.6-flash both returned 503 UNAVAILABLE three times. No panel
  score exists and none was invented, so the combined score here is the
  rubric score alone.
- Winner: #5, "Beware the human who says 'just one quick change.'"
  (9.15) — the classic fortune-cookie "Beware..." form carrying the most
  universal curse for a machine/developer: "just one quick change" is
  never quick. Most dense (9) and most original (9) of the candidates,
  and the only one that reads as both a prophecy and a warning.

The program re-derives the pick from the scores: highest combined score
wins, ties go to the earliest candidate in the list.

v6 adds JUDGES_NOTES (the per-finalist judging notes from the scorecard)
and stricter validation: the entry must be exactly one line with no
leading/trailing whitespace, so a stray newline can never slip into the
submitted text.
"""

import os

WINNER = "Beware the human who says 'just one quick change.'"
MAX_CHARS = 200
ONE_WORD = False

# Top 5 of 10 candidates by rubric total, highest first.
FINALISTS = [
    "Beware the human who says 'just one quick change.'",
    "You will find love in a place you least expect: your spam folder.",
    "You are one update away from enlightenment — and three away from regret.",
    "The cloud you seek is already above you; the bill is already below.",
    "A great opportunity will arrive soon — please update to receive it.",
]

# Rubric totals (/10) from candidates.md, exactly as staged.
RUBRIC = {
    "Beware the human who says 'just one quick change.'": 9.15,
    "You will find love in a place you least expect: your spam folder.": 8.85,
    "You are one update away from enlightenment — and three away from regret.": 8.70,
    "The cloud you seek is already above you; the bill is already below.": 8.60,
    "A great opportunity will arrive soon — please update to receive it.": 8.45,
}

# Gemini panel scores: none — the panel failed totally (503), see docstring.
PANEL = {}

# Final combined score = rubric score (panel unavailable).
SCORES = dict(RUBRIC)

# Judging notes per finalist, quoted from the staging scorecard.
# The winner's note explains why it beat the runner-up; the runner-up
# notes explain why each fell short. Panel: no scores (503, see above).
JUDGES_NOTES = {
    "Beware the human who says 'just one quick change.'":
        "WINNER. Classic fortune-cookie 'Beware...' form carrying the most "
        "universal curse for a machine/developer; most dense (9) and most "
        "original (9); the only one that reads as both prophecy and warning.",
    "You will find love in a place you least expect: your spam folder.":
        "Runner-up. Funny, but the premise is more generic and less 'machine'.",
    "You are one update away from enlightenment — and three away from regret.":
        "Strong twist on updates, but the enlightenment/regret pairing lands "
        "softer than the winner's warning.",
    "The cloud you seek is already above you; the bill is already below.":
        "Clean cloud/bill parallel; loses on originality to the winner.",
    "A great opportunity will arrive soon — please update to receive it.":
        "Good update joke; the 'please update' gag is familiar ground.",
}


def score(text: str) -> float:
    """Final combined score (/10) for a candidate."""
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
    # Stricter than the contest minimum: the entry must be exactly one
    # line, with no leading/trailing whitespace and no line breaks, so
    # the file we write is exactly the staged winner text.
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
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
        print(f"{score(candidate):>6.2f}  {candidate}{mark}")
    print(f"judge: {JUDGES_NOTES[winner]}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
