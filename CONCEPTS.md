# Jury gate — three concepts, one winner

The house judge compares two lines at a time and asks: does it name the real
failure in plain words (what broke and what to do next), is it funny on a
single read with a repeatable twist, is there any padding, and would a team
actually ship it in a real error dialog?

## #1 — DISCARD (cliché AI version)

> Something went wrong. Please try again.

The default LLM shrug. It names no failure, tells the user nothing about what
to do differently, and the "joke" is that there isn't one. Padding in three
words. Discarded before the first comparison.

## #2 — runner-up (clever, but incomplete)

> You're looking at Tuesday's data — the cache is stale.

A real mechanism, a repeatable twist ("Tuesday" is always the day before), and
it reads in one breath. But it never says what the user should DO next, and it
describes a failure the user cannot fix from the dialog. Diagnosis without an
action loses to #3 head-to-head.

## #3 — CHOSEN

> Disk full: we'd write a longer error, but there's no room — same reason your save failed.

Truth: the save failed because the disk is full, stated first and in plain
words. Funny: the line explains its own brevity with the very condition that
broke the save. Repeatable twist: every re-read loops the same way — "why is
this message short?" / "because the disk is full" / "so why did the save fail?"
/ "because the disk is full." No padding: every clause carries either the cause
or the joke, and the two are the same clause. Shippable: a real team would put
this in a dialog because it gives the one action that fixes it — free up space.

Verdict: #3 wins on truth (names the cause and the next step), funny (the
explanation is the joke), and repeatability (the twist survives re-reading).
#1 is the cliché we throw out; #2 stays only as the near-miss that proves why
"what do I do now?" is a required clause.
