# Bug Validator

**Validate your audit findings against Code4rena's official judging criteria before you submit.**

Bug Validator takes any audit report in `.md` format — from any AI tool or written manually — and runs every finding through the official Code4rena judging criteria. It gives you an acceptance score, flags what's wrong, and tells you exactly how to improve each finding before it reaches a judge.

The goal isn't to replace your judgment. It's to give you structured feedback so you can make better submission decisions yourself.

---

## The Problem

Judging in competitive audits is taking longer than ever. The rise of AI-assisted auditing has made it trivially easy to generate large volumes of findings — and a significant portion of wardens are submitting low-quality, unfiltered reports just to angle for payouts. Judges are drowning in noise.

The consequence is real: judging timelines stretch, standards tighten, and wardens with legitimate findings get caught in the slowdown. More importantly, every invalid or low-quality submission you make hurts your signal score — which directly affects your access to restricted contests.

A finding can be technically real and still get rejected because:

- The severity is inflated relative to C4's definitions
- The root cause is identified but the maximum impact isn't demonstrated
- It triggers an automatic invalidator (fee-on-transfer token, admin mistake, dust loss, etc.)
- The PoC works in isolation but requires unrealistic preconditions in production

Bug Validator helps you filter before it counts.

---

## How It Works

Bug Validator reads your `.md` audit report and runs a 4-phase pipeline on every finding:

**Phase 1 — Automatic Invalidator Scan**
Checks 13 hard rules from C4's official criteria. If any triggers, the finding is capped or invalidated regardless of technical merit.

**Phase 2 — Severity Alignment**
Compares the claimed severity against C4's actual definitions. Inflation is one of the most common rejection reasons and heavily penalizes quality scores.

**Phase 3 — Quality Signal Assessment**
Evaluates root cause clarity, maximum impact demonstration, PoC realism, remediation correctness, and writing quality.

**Phase 4 — Score + Verdict**
Outputs an acceptance score (0–100%) and a verdict for each finding:

```
✅ LIKELY VALID      70%+
⚠️ BORDERLINE        40–69%
❌ LIKELY REJECTED   <40%
```

The output is a `Validation-Report.md` saved next to your input report — with detailed feedback on what's hurting each finding and concrete suggestions to improve it. Use that feedback to decide what to submit and how to strengthen your writeups.

---

## Demo

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~                        ██████╗ ██╗   ██╗ ██████╗                         ~~~
~~~                  ▄ ██╗▄██╔══██╗██║   ██║██╔════╝ ▄ ██╗▄                  ~~~
~~~                   ████╗██████╔╝██║   ██║██║  ███╗ ████╗                  ~~~
~~~                  ▀╚██╔▀██╔══██╗██║   ██║██║   ██║▀╚██╔▀                  ~~~
~~~                    ╚═╝ ██████╔╝╚██████╔╝╚██████╔╝  ╚═╝                   ~~~
~~~                        ╚═════╝  ╚═════╝  ╚═════╝                         ~~~
~~~  ██╗   ██╗ █████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗   ~~~
~~~  ██║   ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗  ~~~
~~~  ██║   ██║███████║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝  ~~~
~~~  ╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗  ~~~
~~~   ╚████╔╝ ██║  ██║███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║  ~~~
~~~    ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

         Code4rena Acceptance Predictor — by mettal

Which .md report file should I validate?
Enter path (e.g. ./audit/report.md): ./audit/AUDIT_REPORT.md

> Analyzing: ./audit/AUDIT_REPORT.md
> Output: ./audit/Validation-Report.md
```

**Output summary:**

```
| ID   | Title                              | Claimed  | Predicted | Score | Verdict           |
|------|------------------------------------|----------|-----------|-------|-------------------|
| C-01 | Reentrancy in withdraw function    | Critical | Critical  | 94%   | ✅ LIKELY VALID   |
| H-01 | Access control missing on setter   | High     | High      | 81%   | ✅ LIKELY VALID   |
| M-01 | Oracle price staleness             | Medium   | Medium    | 73%   | ✅ LIKELY VALID   |
| M-02 | Non-standard token breaks accounting | Medium | QA        | 18%   | ❌ LIKELY REJECTED|
| L-04 | Unbounded loop in state update     | Low      | Low       | 61%   | ⚠️ BORDERLINE     |
```

---

## Installation

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated (Pro, Max, or Team subscription).

```bash
git clone https://github.com/santiagoib/bug-validator.git
cd bug-validator
chmod +x install.sh
./install.sh
source ~/.bashrc   # or ~/.zshrc
```

That's it. No API key. No additional dependencies.

---

## Usage

**Option 1 — Terminal (recommended)**

```bash
bug-validator                          # prompts for file path
bug-validator ./audit/AUDIT_REPORT.md  # direct path
```

**Option 2 — Claude Code skill**

```
claude
/bug-validator
```

The output `Validation-Report.md` is saved in the same directory as your input report — with scores, verdicts, and detailed per-finding feedback.

---

## What It Checks

Bug Validator applies the official Code4rena judging criteria:

**13 Automatic Invalidators** — hard rules that cap or kill findings regardless of technical merit:
- Fee-on-transfer / non-standard tokens (unless in scope)
- Admin/owner privilege misuse → QA only
- Approve race condition → always invalid
- Dust loss only → QA/Low
- Speculation on future code
- User mistake required → invalid or QA at best
- Root cause in out-of-scope library
- And more

**Severity Alignment** — C4's actual definitions, not intuition:
- High: direct asset loss with no hand-wavy hypotheticals
- Medium: indirect impact with stated assumptions
- QA: anything else

**Quality Signals** — what judges actually look for:
- Root cause identified vs symptom described
- Maximum achievable impact demonstrated
- PoC realistic in production context
- Remediation correct and present

---

## Works With Any Report

Bug Validator accepts any `.md` audit report — whether it was generated by an AI tool or written manually. As long as findings are documented in markdown, it can validate them.

---

## License

MIT
