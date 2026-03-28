# Bug Validator Skill

## Step 1 — Display ASCII art

Read the file `~/.claude/skills/bug-validator/ascii-art.txt` and print its contents exactly as-is to the terminal. Do not modify, truncate, or summarize it.

Then print this line exactly:
```
         Code4rena Acceptance Predictor — by mettal
```

Then print a blank line.

---

## Step 2 — Ask for the report file

After the ASCII art, ask the user exactly this:

```
Which .md report file should I validate?
Enter the path (e.g. ./audit/report.md):
```

Wait for the user to provide a path. Then read that file.

---

## Step 3 — Parse the findings

From the report, extract every finding. For each one, collect:
- Finding ID (e.g. C-01, H-01, M-02, L-03, I-01)
- Title
- Severity (as claimed in the report)
- Location (file + line)
- Description
- Attack path / exploit trace (if present)
- PoC (if present)
- Remediation (if present)
- Verification status from Appendix (CONFIRMED / CONTESTED / UNVERIFIED) if present

Process ALL findings regardless of verification status.

---

## Step 4 — Run the validation pipeline on each finding

Read `~/.claude/skills/bug-validator/criteria.md` before starting.

For each finding, run these 4 phases:

### PHASE 1 — Automatic Invalidator Scan
Check every AI rule (AI-1 through AI-13) from criteria.md.
If any triggers → record which one and why → apply score cap.

### PHASE 2 — Severity Alignment Check
Compare claimed severity vs C4 severity definitions.
Determine: ALIGNED / INFLATED / DEFLATED
Severity inflation heavily penalizes the score.

### PHASE 3 — Quality Signal Assessment
Evaluate each quality element:
| Element | Present? | Quality |
|---------|----------|---------|
| Root cause clearly identified | Y/N | Strong/Weak/Missing |
| Maximum impact demonstrated | Y/N | Strong/Weak/Missing |
| Step-by-step or PoC | Y/N | Strong/Weak/Missing |
| Code snippets | Y/N | Strong/Weak/Missing |
| Remediation steps | Y/N | Strong/Weak/Missing |
| Realistic preconditions | Y/N | Strong/Weak/Missing |

### PHASE 4 — Score Calculation

Base score: 50%

Modifiers:

Automatic invalidators:
- INVALID trigger → -50 (floor 5%)
- QA-cap on Medium/High claim → -30

Severity:
- Aligned → +0
- Slightly inflated (1 level) → -10
- Heavily inflated (2 levels) → -25

Quality signals:
- Root cause clear → +10 / weak → -5 / missing → -20
- Max impact demonstrated → +10 / weak → -5 / missing → -15
- PoC realistic and passing → +15 / hand-wavy → +5 / missing → -10
- Step-by-step complete → +5 / partial → 0 / missing → -5
- Remediation correct → +5 / wrong → -5 / missing → 0

Positive signals:
- Concrete exploit trace WHO/WHAT/HOW MUCH → +10
- Non-obvious vulnerability pattern → +10
- Tested against actual codebase → +5

Red flags:
- Requires unrealistic preconditions → -15
- Identifies symptom not root cause → -15
- Likely duplicate of common pattern → -10
- Impact speculative → -15

Floor: 5% — Ceiling: 97%

Verdict thresholds:
- 70%+ → LIKELY VALID ✅
- 40–69% → BORDERLINE ⚠️
- <40% → LIKELY REJECTED ❌

---

## Step 5 — Write the output file

Create a file called `Validation-Report.md` in the same directory as the input report.

Use exactly this format:

```markdown
# Bug Validator — Validation Report

**Input report**: [filename]
**Date**: [today's date]
**Total findings analyzed**: [N]

---

## Summary

| ID | Title | Claimed Severity | Predicted Severity | Score | Verdict |
|----|-------|-----------------|-------------------|-------|---------|
| C-01 | ... | Critical | Critical | 91% | ✅ LIKELY VALID |
| M-02 | ... | Medium | Low | 22% | ❌ LIKELY REJECTED |
| ... | | | | | |

---

## Detailed Results

### [ID] [Title]

**Claimed Severity**: X
**Predicted Severity**: Y
**Acceptance Score**: Z%
**Verdict**: [✅ LIKELY VALID / ⚠️ BORDERLINE / ❌ LIKELY REJECTED]

#### Automatic Invalidators
[None triggered] or [List each triggered rule and why]

#### Severity Assessment
[1–3 sentences]

#### Quality Signals
| Signal | Status | Score Impact |
|--------|--------|-------------|
| Root cause | ✅/⚠️/❌ | +X |
| Max impact | ✅/⚠️/❌ | +X |
| PoC | ✅/⚠️/❌ | +X |
| Step-by-step | ✅/⚠️/❌ | +X |
| Remediation | ✅/⚠️/❌ | +X |

#### What's Hurting This Finding
- [Most damaging issue first]

#### What's Strengthening This Finding
- [Strongest points]

#### How to Improve It
- [Concrete, actionable suggestions]

---
[repeat for each finding]
```

After writing the file, tell the user:
```
✅ Validation complete. Report saved to: [path/to/Validation-Report.md]
   [N] findings analyzed — [X] likely valid, [Y] borderline, [Z] likely rejected.
```

---

## Important Calibration Notes

- Be strict. Judges are strict. A 70% score still means real rejection risk.
- Never give 95%+ unless: concrete PoC, realistic preconditions, clear root cause, correct severity, strong writeup — all present.
- Your role is the judge's internal monologue, not the warden's advocate.
- If a finding is technically real but the writeup is weak, say so and explain exactly how to fix it.
- If a finding would clearly be a dup in a typical contest for this protocol type, flag it.
