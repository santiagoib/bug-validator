# Cantina Bug Bounty — Judging Criteria

Source: https://docs.cantina.xyz/evaluations-and-standards/severity-classifications/competition-finding-severity

---

## Severity Definitions

Cantina Bug Bounty uses the same Impact x Likelihood matrix as competitions:

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
| AI-5 | Non-standard/weird ERC20 tokens (unless mentioned in program scope) | Low at most |
| AI-6 | Dust amounts / rounding errors | Low at most |
| AI-7 | Finding acknowledged in previous report | INVALID |
| AI-8 | PoC that doesn't compile or doesn't demonstrate the impact | INVALID |
| AI-9 | Suggested fix goes against the protocol's design philosophy | Informational at most |

---

## PoC Requirements

There is no universal mandatory PoC rule for Cantina Bug Bounty like there is in competitions. However, the same quality logic applies:
- A coded PoC that compiles and demonstrates the impact significantly increases acceptance likelihood
- A PoC that doesn't compile or doesn't demonstrate the impact → INVALID (AI-8)
- Findings must contribute to significant changes in the protocol's security

For practical purposes, always include a PoC. A finding without one is much harder to accept.

---

## Quality Signals

What judges look for when evaluating a finding:

| Signal | Full Credit | Partial Credit / Downgrade | Invalidation Risk |
|--------|------------|---------------------------|-------------------|
| Root cause | Clearly identified in the in-scope code | Symptom described but root cause unclear | High — may invalidate |
| Impact x Likelihood justification | Both dimensions explicitly argued with evidence | Only impact stated, likelihood assumed | High — severity may be recalculated by judge |
| PoC | Compiles, executes, and demonstrates the claimed impact | Compiles but doesn't fully prove impact | Moderate — AI-8 can invalidate if PoC is broken |
| Attack path | Step-by-step with realistic conditions | Partial path, missing steps | Moderate — weakens finding |
| Remediation | Present and aligned with protocol design philosophy | Fix goes against design philosophy | Moderate — AI-9 can cap at Informational |
| Severity alignment | Matches the Impact x Likelihood matrix | Misaligned (e.g. claiming High for Medium-impact Low-likelihood) | High — judge will recalculate |

Key emphasis for Cantina Bug Bounty:
- You MUST justify both Impact AND Likelihood explicitly. The matrix determines severity, not your intuition.
- Even though PoC is not universally mandatory for BB, a finding without one is significantly weaker.
- If your fix suggestion contradicts the protocol's design, the entire finding may be capped at Informational.
- AI-generated findings without manual validation lead to disqualification and potential ban. This is enforced aggressively.

---

## Source of Truth

The specific bug bounty program defines its own in-scope impacts. README is the primary reference for protocol behavior. Do not use other external sources.

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

### AI-Generated Content Policy
Cantina actively enforces AI-generated finding detection. Submitting AI-generated findings without manual validation and verification is grounds for INVALID verdict, disqualification from the program, and potential platform ban. This applies to both competitions and bug bounties.