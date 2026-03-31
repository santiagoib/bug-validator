# Cantina Competitive — Judging Criteria

Source: https://docs.cantina.xyz/evaluations-and-standards/severity-classifications/competition-finding-severity

---

## Severity Definitions

Cantina uses an Impact x Likelihood matrix to determine severity:

|  | Impact: High | Impact: Medium | Impact: Low |
|---|---|---|---|
| **Likelihood: High** | High | High | Medium |
| **Likelihood: Medium** | High | Medium | Low |
| **Likelihood: Low** | Medium | Low | Informational |

### High (Impact: High)
- Funds can be directly lost

### Medium
- Impact High with Likelihood Low
- Impact Medium with Likelihood Medium or High

### Low
- Impact Low with Likelihood Medium or High
- Impact Medium with Likelihood Low

### Informational
- Impact Low with Likelihood Low
- Design issues without fund loss

**Tiebreak guide:** ask what happens to the protocol if the bug is NOT fixed. If it leads to a catastrophic scenario triggerable by anyone → very likely High. If the protocol can function without fixing it → likely Low.

---

## Automatic Invalidators (AI)

| ID | Rule | Result |
|----|------|--------|
| AI-1 | User error manageable from the frontend | Informational at most |
| AI-2 | Requires admin/owner access to execute (unless the protocol is designed to be resilient to those actions) | Low at most |
| AI-3 | AI-generated finding without manual validation | INVALID + risk of ban |
| AI-4 | Approval/ERC20 race condition | INVALID |
| AI-5 | Non-standard/weird ERC20 tokens (unless mentioned in README) | Low at most |
| AI-6 | Dust amounts / rounding errors | Low at most |
| AI-7 | Finding acknowledged in previous report | INVALID |
| AI-8 | High or Medium without PoC (for researchers with reputation score <80) | INVALID — PoC mandatory |
| AI-9 | PoC that doesn't compile or doesn't demonstrate the impact | INVALID |
| AI-10 | Suggested fix goes against the protocol's design philosophy | Informational at most |

---

## PoC Requirements

By default, ALL Cantina competitions have a mandatory PoC rule:
- **High and Medium** require a coded PoC before the competition ends
- Applies to researchers with reputation score < 80
- Exceptions: missing functions, or researcher with score >= 80
- The PoC MUST compile and demonstrate the impact
- Cantina Dedicated Researchers are exempt (can provide PoC on request)

A PoC that doesn't compile or doesn't demonstrate the impact → INVALID (AI-9).

---

## Quality Signals

What judges look for when evaluating a finding:

| Signal | Full Credit | Partial Credit / Downgrade | Invalidation Risk |
|--------|------------|---------------------------|-------------------|
| Root cause | Clearly identified in the in-scope code | Symptom described but root cause unclear | High — may invalidate |
| Impact x Likelihood justification | Both dimensions explicitly argued with evidence | Only impact stated, likelihood assumed | High — severity may be recalculated by judge |
| PoC | Compiles, executes, and demonstrates the claimed impact | Compiles but doesn't fully prove impact | Critical — AI-8/AI-9 can invalidate |
| Attack path | Step-by-step with realistic conditions | Partial path, missing steps | Moderate — weakens finding |
| Remediation | Present and aligned with protocol design philosophy | Fix goes against design philosophy | Moderate — AI-10 can cap at Informational |
| Severity alignment | Matches the Impact x Likelihood matrix | Misaligned (e.g. claiming High for Medium-impact Low-likelihood) | High — judge will recalculate |

Key emphasis for Cantina:
- You MUST justify both Impact AND Likelihood explicitly. A finding with High impact but Low likelihood is Medium, not High.
- Your PoC is not optional if you're below reputation 80. No PoC = no consideration.
- If your fix suggestion contradicts the protocol's design, the entire finding may be capped at Informational.

---

## Source of Truth

README is the primary reference for protocol behavior. Do not use other external sources.

---

## Scope

- If a contract is in-scope, all its parent contracts are included
- Vulnerability in a library used by an in-scope contract → valid
- Contract out of scope → INVALID

---

## Duplicate Rules

- Findings are duplicates if they share the same root cause
- Fixing the root cause would make both unexploitable

---

## Platform-Specific Rules

### Escalation Process
After judging there is an escalation phase where verdicts can be contested. There is a penalty for invalid escalations. Consider this when recommending whether to escalate: weak evidence + escalation penalty can be worse than accepting the original verdict.