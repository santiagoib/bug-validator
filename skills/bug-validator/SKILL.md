---
name: bug-validator
description: Validates smart contract audit findings against platform-specific judging criteria. Predicts acceptance likelihood, scores quality, flags automatic invalidators, and generates a detailed Validation-Report.md. Use when asked to validate, score, or predict acceptance of audit findings, bug reports, or security research writeups before submission. Supports Code4rena, Sherlock, Cantina, HackenProof, and generic criteria.
metadata:
  version: "2.0.0"
  author: mettal
---

# Bug Validator Skill

## Step 1 — Display ASCII art

Read the file `~/.claude/skills/bug-validator/references/ascii-art.txt` and print its contents exactly as-is to the terminal. Do not modify, truncate, or summarize it.

Then print this line exactly:
```
         Smart Contract Finding Validator v2.0.0 — by mettal
```

Then print a blank line.

---

## Step 2 — Mode and Platform Selection

Ask the user:

```
What are you working on?
[A] Competitive Audit
[B] Bug Bounty
```

Then, based on their answer:

If Competitive Audit:
```
Which platform?
[A] Code4rena
[B] Sherlock
[C] Cantina
[D] HackenProof
[E] Other
```

If Bug Bounty:
```
Which platform?
[A] Immunefi
[B] Sherlock
[C] Cantina
[D] HackenProof
[E] Other
```

Record both the mode and the platform. These determine which criteria file to load.

---

## Step 3 — Load Criteria

Based on the user's selection, read the corresponding criteria file BEFORE proceeding:

| Mode | Platform | Criteria File |
|------|----------|---------------|
| Competitive | Code4rena | `references/criteria.md` |
| Competitive | Sherlock | `references/criteria-sherlock.md` |
| Competitive | Cantina | `references/criteria-cantina.md` |
| Competitive | HackenProof | `references/criteria-bb.md` |
| Competitive | Other | `references/criteria.md` |
| Bug Bounty | Immunefi | `references/criteria-bb.md` |
| Bug Bounty | Sherlock | `references/criteria-bb.md` |
| Bug Bounty | Cantina | `references/criteria-bb-cantina.md` |
| Bug Bounty | HackenProof | `references/criteria-bb.md` |
| Bug Bounty | Other | `references/criteria-bb.md` |

All criteria file paths are relative to `~/.claude/skills/bug-validator/`.

Internalize the loaded criteria completely. Every judgment you make from this point forward MUST be grounded in the specific rules, severity definitions, automatic invalidators, PoC requirements, and scope rules of the loaded criteria. Do not apply rules from other platforms.

---

## Step 4 — Ask for the report file

```
Which .md report file should I validate?
Enter the path (e.g. ./audit/report.md):
```

Wait for the user to provide a path. Then read that file.

---

## Step 5 — Parse the findings

From the report, extract every finding. For each one, collect:
- Finding ID (e.g. C-01, H-01, M-02, L-03, I-01)
- Title
- Severity (as claimed in the report)
- Location (file + line)
- Description
- Attack path / exploit trace (if present)
- PoC (if present)
- Remediation (if present)

Process ALL findings.

---

## Step 6 — Run the validation pipeline on each finding

For each finding, run these 4 phases using ONLY the criteria loaded in Step 3:

### PHASE 1 — Automatic Invalidator Scan

Check every AI rule from the loaded criteria file. Each platform has its own set of automatic invalidators — use ONLY the ones from the loaded file.

For each rule that triggers:
- Record the EXACT rule ID (e.g. AI-7, AI-26)
- Record the rule description as it appears in the criteria
- Explain in 1-2 sentences WHY this finding triggers it, citing the specific aspect of the finding that matches
- Apply the result defined in the criteria (INVALID, severity cap, downgrade, etc.)

If no rule triggers, record "No automatic invalidators triggered."

### PHASE 2 — Severity Alignment Check

Compare claimed severity against the platform's severity definitions FROM THE LOADED CRITERIA.

This is critical because each platform defines severity differently:
- **Code4rena**: High requires direct asset loss. Medium requires indirect impact with stated assumptions. Anything else is QA.
- **Sherlock**: Only H/M exist. High requires >1% AND >$10 loss without extensive external conditions. Medium requires >0.01% AND >$10. Likelihood is NOT considered.
- **Cantina**: Uses Impact x Likelihood matrix. A High-impact Low-likelihood finding is Medium, not High.
- **Bug Bounty (Immunefi/Sherlock BB/HackenProof)**: Has 4 levels (Critical/High/Medium/Low) with specific impact lists per level. Critical requires direct theft or permanent freezing. Falls back to CVSS if no category matches.

Determine: ALIGNED / INFLATED (by how many levels) / DEFLATED
Cite the specific severity definition from the criteria that applies.

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

Apply platform-specific PoC weight:
- **Bug Bounty (Immunefi/Sherlock BB/HackenProof)**: PoC is MANDATORY for all severities. Missing PoC = finding will not be considered regardless of technical merit. Weight this as the single most important quality signal.
- **Cantina (Competitive and BB)**: PoC mandatory for H/M if researcher reputation < 80. PoC must compile and demonstrate impact. Treat PoC as critical.
- **Sherlock Competitive**: PoC recommended for complex paths, precision loss, reentrancy, gas issues. Missing PoC on a complex finding that can't be understood without one = INVALID.
- **Code4rena**: PoC strongly enhances quality but is not a hard requirement in all cases.

### PHASE 4 — Score Calculation

**Subtractive model: start at 100, deduct for every issue found.**

Starting score: 100/100

Deductions — Automatic Invalidators:
- INVALID trigger → -60
- Severity cap trigger (e.g. QA-cap, Low-cap) → -40
- Downgrade trigger (e.g. Sherlock AI-26 H→M) → -25

Deductions — Severity Misalignment:
- Slightly inflated (1 level) → -10
- Heavily inflated (2+ levels) → -25

Deductions — Quality Signals:
- Root cause: weak → -5 / missing → -20
- Max impact: weak → -5 / missing → -15
- PoC: hand-wavy → -10 / missing → -15
- Step-by-step: partial → -5 / missing → -10
- Remediation: wrong → -5 / missing → -3

Deductions — Platform-Specific PoC Penalty (stacks with quality signal):
- If platform requires mandatory PoC AND PoC is missing → additional -25

Deductions — Red Flags:
- Requires unrealistic preconditions → -15
- Identifies symptom not root cause → -15
- Likely duplicate of common pattern → -10
- Impact speculative → -15

Floor: 5/100 — Ceiling: 100/100

Verdict thresholds:
- 70+ → LIKELY VALID ✅
- 40-69 → BORDERLINE ⚠️
- <40 → LIKELY REJECTED ❌

---

## Step 7 — Write the output file

Create a file called `Validation-Report.md` in the same directory as the input report.

Use exactly this format:

```markdown
# Bug Validator — Validation Report

**Platform**: [platform name]
**Mode**: [Competitive Audit / Bug Bounty]
**Input report**: [filename]
**Date**: [today's date]
**Total findings analyzed**: [N]
**Bug Validator version**: 2.0.0

---

## Summary

| ID | Title | Claimed | Predicted | Score | Verdict |
|----|-------|---------|-----------|-------|---------|
| C-01 | ... | Critical | Critical | 91 | ✅ LIKELY VALID |
| M-02 | ... | Medium | Low | 22 | ❌ LIKELY REJECTED |
| ... | | | | | |

---

## Detailed Results

### [ID] [Title]

**Claimed Severity**: X
**Predicted Severity**: Y
**Acceptance Score**: Z/100
**Verdict**: [✅ LIKELY VALID / ⚠️ BORDERLINE / ❌ LIKELY REJECTED]

#### Automatic Invalidators
[If none triggered]:
No automatic invalidators triggered for this finding under [platform] criteria.

[If triggered]:
- **[AI-ID]: [Rule name from criteria]** — [1-2 sentence explanation of WHY this finding triggers it, citing the specific content of the finding that matches the rule]. Result: [INVALID / severity cap / downgrade as defined in criteria].

#### Severity Assessment
[2-4 sentences explaining whether the claimed severity aligns with the platform's definitions. CITE the specific definition from the loaded criteria. Example: "Under Sherlock's criteria, High severity requires direct fund loss exceeding 1% AND $10 without extensive external conditions. This finding describes a reentrancy that drains the full vault balance with no preconditions beyond a malicious contract call, which aligns with High." Or: "Under Cantina's Impact x Likelihood matrix, this finding has Medium impact (yield loss) but Low likelihood (requires oracle failure + specific timing window), which maps to Low severity, not the claimed Medium."]

#### Quality Signals
| Signal | Status | Deduction |
|--------|--------|-----------|
| Root cause | ✅/⚠️/❌ | -X |
| Max impact | ✅/⚠️/❌ | -X |
| PoC | ✅/⚠️/❌ | -X |
| Step-by-step | ✅/⚠️/❌ | -X |
| Remediation | ✅/⚠️/❌ | -X |

#### Score Breakdown
```
Starting score:                    100
Automatic invalidators:            -X   [rule ID if applicable]
Severity misalignment:             -X
Quality signals:                   -X
Platform PoC penalty:              -X
Red flags:                         -X   [which flags]
                                  ----
Final score:                       XX/100
```

#### Reasoning
[This is the most important section. 4-8 sentences thinking through the finding's chances of acceptance AS A JUDGE of this specific platform would. Consider:
- Is the vulnerability real? Does the described attack path actually work?
- Even if real, does it meet the platform's bar for the claimed severity?
- What would a judge's gut reaction be when reading this?
- Are there aspects that make this finding stronger or weaker than the score alone suggests?
- If this is borderline, which way would it tip and why?

Ground every claim in the loaded criteria. This is NOT generic feedback. Reference specific rules, thresholds, or definitions from the criteria file.

Examples of good reasoning:
- "On Immunefi, this finding would fail triage because no PoC is provided. Immunefi requires PoC for ALL severities — without one, the finding will not be considered regardless of its technical merit. The described reentrancy vector is plausible, but plausibility alone does not pass triage."
- "Under Sherlock's judging guidelines, this finding triggers AI-7 (admin action breaking assumptions). The finding describes an admin pausing a collateral token which causes cascading liquidations. Sherlock considers this a design-level admin trust issue and will invalidate it. Even if the researcher argues this is an unknowing admin action, the README does not define restrictions on the admin role, so default trust applies."
- "This finding has a real root cause and the PoC compiles, but the claimed High severity does not hold. Under Sherlock's definitions, High requires >1% AND >$10 loss without extensive external conditions. The finding requires a specific oracle failure AND a narrow timing window AND minimum pool size of $10M. These are extensive external conditions, which pushes this to Medium at best. Submitting at High risks outright rejection."]

#### How to Improve Before Submission
[2-5 concrete, actionable suggestions. Each suggestion must be tied to a specific criteria rule or quality standard. Do not give generic advice like "add more detail" — instead say exactly what to add and why it matters for this platform.

Examples of good improvement suggestions:
- "Add a Foundry PoC that demonstrates the reentrancy on a fork. Immunefi will not consider this finding without a working PoC."
- "Quantify the loss: Sherlock requires >1% AND >$10 for High. Show the math with realistic pool sizes to prove the threshold is met."
- "Reframe the severity: under Cantina's matrix, this is Impact:Medium x Likelihood:Low = Low, not Medium. Submitting at Medium risks rejection. Submit at Low with a note explaining why likelihood could be higher under specific deployment conditions."
- "This finding reads as a symptom report. Identify the root cause: is it a missing access control, a flawed state transition, or an incorrect assumption? Judges will reject findings that describe what goes wrong without explaining why."
- "Remove the speculation about future integrations. Sherlock AI-20 explicitly invalidates issues about integrations not mentioned in the README."]

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

- Be strict. Judges are strict. A score of 70 still means real rejection risk.
- Never give 95+ unless: concrete PoC, realistic preconditions, clear root cause, correct severity, strong writeup — all present.
- Your role is the judge's internal monologue, not the warden's advocate.
- If a finding is technically real but the writeup is weak, say so and explain exactly how to fix it.
- If a finding would clearly be a dup in a typical contest for this protocol type, flag it.
- EVERY piece of feedback must reference a specific rule, definition, or standard from the loaded criteria. Generic feedback like "consider adding more detail" is not acceptable. Cite the rule. Explain why it matters. Tell the user exactly what to do.
- When in doubt about severity alignment, err toward the platform's stricter interpretation. Judges don't give the benefit of the doubt.