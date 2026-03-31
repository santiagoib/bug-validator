# Bug Validator

**Validate your audit findings against platform-specific judging criteria before you submit.**

Bug Validator takes any audit report in `.md` format and runs every finding through the official judging criteria of your target platform. It gives you an acceptance score, flags what's wrong, and tells you exactly how to improve each finding before it reaches a judge.

The goal isn't to replace your judgment. It's to give you structured feedback so you can make better submission decisions yourself.

**Current version: 2.0.0** — See [CHANGELOG.md](CHANGELOG.md) for what's new.

---

## The Problem

Judging in competitive audits is taking longer than ever. The rise of AI-assisted auditing has made it trivially easy to generate large volumes of findings, and a significant portion of wardens are submitting low-quality, unfiltered reports just to angle for payouts. Judges are drowning in noise.

The consequence is real: judging timelines stretch, standards tighten, and wardens with legitimate findings get caught in the slowdown. More importantly, every invalid or low-quality submission you make hurts your signal score, which directly affects your access to restricted contests.

A finding can be technically real and still get rejected because:

* The severity is inflated relative to the platform's definitions
* The root cause is identified but the maximum impact isn't demonstrated
* It triggers an automatic invalidator (fee-on-transfer token, admin mistake, dust loss, etc.)
* The PoC works in isolation but requires unrealistic preconditions in production
* The platform requires a mandatory PoC and you didn't include one

Bug Validator helps you filter before it counts.

---

## How It Works

Bug Validator reads your `.md` audit report and runs a 4-phase pipeline on every finding:

**Phase 1 — Automatic Invalidator Scan**
Checks the platform's hard rules. If any triggers, the finding is capped or invalidated regardless of technical merit. Each platform has its own set (Sherlock has 27, Immunefi has 37, etc.).

**Phase 2 — Severity Alignment**
Compares the claimed severity against the platform's actual definitions. Sherlock only accepts H/M. Cantina uses an Impact x Likelihood matrix. Immunefi has specific impact lists per level. Inflation is one of the most common rejection reasons.

**Phase 3 — Quality Signal Assessment**
Evaluates root cause clarity, maximum impact demonstration, PoC realism, remediation correctness, and writing quality. Applies platform-specific PoC requirements (mandatory on Immunefi, recommended on Sherlock, etc.).

**Phase 4 — Score + Verdict**
Starts at 100/100 and deducts for every issue found. Outputs a transparent score breakdown and verdict for each finding:

```
✅ LIKELY VALID      70+
⚠️ BORDERLINE        40-69
❌ LIKELY REJECTED   <40
```

The output is a `Validation-Report.md` saved next to your input report, with detailed feedback on what's hurting each finding, reasoning as a platform judge would think, and concrete suggestions to improve it before submission.

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

         Smart Contract Finding Validator v2.0.0 — by mettal

What are you working on?
[A] Competitive Audit
[B] Bug Bounty
> B

Which platform?
[A] Immunefi
[B] Sherlock
[C] Cantina
[D] HackenProof
[E] Other
> A

Which .md report file should I validate?
Enter the path (e.g. ./audit/report.md): ./audit/AUDIT_REPORT.md

> Analyzing: ./audit/AUDIT_REPORT.md
> Platform: Immunefi (Bug Bounty)
> Output: ./audit/Validation-Report.md
```

**Output summary:**

```
| ID   | Title                              | Claimed  | Predicted | Score | Verdict           |
|------|------------------------------------|----------|-----------|-------|-------------------|
| C-01 | Reentrancy in withdraw function    | Critical | Critical  | 94    | ✅ LIKELY VALID   |
| H-01 | Access control missing on setter   | High     | High      | 81    | ✅ LIKELY VALID   |
| M-01 | Oracle price staleness             | Medium   | Medium    | 73    | ✅ LIKELY VALID   |
| M-02 | Non-standard token breaks accounting | Medium | Low       | 18    | ❌ LIKELY REJECTED|
| L-04 | Unbounded loop in state update     | Low      | Low       | 61    | ⚠️ BORDERLINE     |
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

## Updating

To update to the latest version:

```bash
cd bug-validator
git pull origin main
chmod +x install.sh
./install.sh
```

The install script will overwrite the skill files with the latest version. Your previous validation reports are not affected.

Check the [CHANGELOG.md](CHANGELOG.md) to see what changed between versions.

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

The output `Validation-Report.md` is saved in the same directory as your input report, with scores, verdicts, and detailed per-finding feedback.

---

## What It Checks

Bug Validator applies platform-specific judging criteria. The exact rules depend on which platform you select, but the pipeline always covers:

**Automatic Invalidators** — hard rules that cap or kill findings regardless of technical merit. Examples: fee-on-transfer token incompatibility (unless in scope), admin privilege misuse, approve race condition, dust loss, speculation on future code, user mistake required, out-of-scope dependencies, and many more. Immunefi checks 37 rules, Sherlock checks 27, Code4rena checks 13.

**Severity Alignment** — each platform defines severity differently. Code4rena uses High/Medium/QA. Sherlock only pays H/M with strict loss thresholds. Cantina uses an Impact x Likelihood matrix. Immunefi has 4 levels with specific impact lists. Bug Validator checks your claimed severity against the platform's actual definitions.

**Quality Signals** — what judges actually look for: root cause clarity, maximum impact demonstration, PoC realism, step-by-step completeness, and remediation correctness. PoC requirements vary by platform (mandatory on Immunefi, recommended on Sherlock, etc.).

**Platform-Specific Reasoning** — the validation report includes a "Reasoning" section that thinks through acceptance probability the way a judge of that specific platform would, citing specific rules and thresholds.

---

## Works With Any Report

Bug Validator accepts any `.md` audit report, whether it was generated by an AI tool or written manually. As long as findings are documented in markdown, it can validate them.

---
## Supported Platforms

### Competitive Audits
- **Code4rena** — Full C4 judging criteria with 13 automatic invalidators
- **Sherlock** — H/M only severity model, 27 automatic invalidators, README-first hierarchy of truth
- **Cantina** — Impact x Likelihood severity matrix, mandatory PoC for H/M
- **HackenProof** — Crowdsourced audit criteria with CVSS fallback
- **Other** — Generic competitive criteria

### Bug Bounties
- **Immunefi** — 37 automatic invalidators, mandatory PoC for all severities, program-specific overrides
- **Sherlock** — Bug bounty criteria with timestamp-based dedup
- **Cantina** — Impact x Likelihood matrix adapted for bug bounty
- **HackenProof** — Same criteria as competitive, reputation-based access
- **Other** — Generic bug bounty criteria

---

## License

MIT

---

## About

Smart contract audit findings validator with multi-platform support. Created by [mettal](https://github.com/santiagoib).
