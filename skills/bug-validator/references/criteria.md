# Code4rena Competitive — Judging Criteria

Source: https://docs.code4rena.com/competitions/judging-criteria
Source: https://docs.code4rena.com/competitions/severity-categorization

---

## Severity Definitions

### High (3)
- Assets (funds, NFTs, data, authorization) can be stolen/lost/compromised DIRECTLY
- OR indirectly, but ONLY with a valid attack path — no hand-wavy hypotheticals
- Loss of matured yield at real amounts → High
- Loss of dust → QA/Low regardless

### Medium (2)
- Assets NOT at direct risk
- BUT function of protocol or availability is impacted
- OR leaks value with a hypothetical attack path with STATED assumptions and external requirements
- Privilege escalation may be Medium depending on likelihood + impact
- Any privileged function scenario with reasonable assumptions → up to Medium

### QA / Low
- Assets not at risk
- State handling issues
- Function incorrect as to spec
- Governance/centralization risk (admin privileges)
- Informational (code style, clarity, syntax, versioning, events)

---

## Automatic Invalidators (AI)

| ID | Rule | Result |
|----|------|--------|
| AI-1 | Root cause is in an out-of-scope library/contract (not in how the in-scope contract uses it) | INVALID — OOS |
| AI-2 | Finding requires the user to make a mistake or enter wrong input | INVALID or QA at best |
| AI-3 | Non-standard / weird ERC-20 token or fee-on-transfer token, unless explicitly listed as supported in scope (USDT is always in scope) | INVALID |
| AI-4 | Admin/owner direct misuse of privileges (reckless admin mistake) | QA only — not Medium/High |
| AI-5 | Approve / safeApprove front-run race condition | INVALID |
| AI-6 | Unused view function finding | QA/Low only |
| AI-7 | Faulty event emission with no broader on-chain impact | Capped Low |
| AI-8 | Speculation on future code not in scope | INVALID unless root cause is demonstrably in scope |
| AI-9 | Loss of dust only (rounding errors, marginal fee variations) | QA/Low only |
| AI-10 | Loss of unmatured yield or yield in motion | Capped Medium |
| AI-11 | Finding published in a prior audit report listed in README (acknowledged/wontfix) | OOS / Known issue |
| AI-12 | CryptoPunks non-support | INVALID — Informational only |
| AI-13 | Phishing or improper user caution | INVALID |

---

## PoC Requirements

PoC is not strictly mandatory on Code4rena, but strongly recommended.

A finding without a PoC can still be accepted if the root cause and impact are clearly explained. However, a coded PoC significantly increases acceptance likelihood, especially for:
- Complex attack paths
- Precision loss or rounding issues
- Reentrancy vectors
- Any finding where the burden of proof is non-trivial

A PoC that does not pass burden of proof → insufficient quality → grounds for downgrade or invalidation.

---

## Quality Signals

What judges look for when evaluating a finding:

| Signal | Full Credit | Partial Credit / Downgrade | Invalidation Risk |
|--------|------------|---------------------------|-------------------|
| Root cause | Clearly identified and explained | Missing or unclear | High — may invalidate |
| Maximum impact | Worst-case scenario demonstrated with realistic numbers | Impact mentioned but not maximized | Moderate — downgrade likely |
| Attack path | Step-by-step from root cause to impact, or coded PoC | Hand-wavy or partial explanation | High — insufficient quality |
| Code snippets | Relevant code referenced with line numbers | Generic references without specifics | Low — but weakens credibility |
| Remediation | Present and correct | Wrong or missing | Low — does not invalidate but loses credit |
| Severity alignment | Matches C4 definitions exactly | Inflated by 1 level | High — inflation heavily penalized |

Grounds for invalidation despite technical validity:
- Finding does not add value to the sponsor
- Finding appears to be a direct copy of another report in the same audit
- Severity is clearly and deliberately inflated

---

## Source of Truth

1. Contest README and scope definition (primary)
2. Code comments
3. C4 default judging criteria

---

## Scope

- Root cause IN an out-of-scope library → finding is OOS (INVALID)
- Root cause in how the IN-SCOPE contract incorrectly uses an OOS library → VALID
- Contracts not listed in scope → INVALID

---

## Duplicate Rules

- Findings are duplicates if they share the same ROOT CAUSE
- Fixing the root cause would make both unexploitable
- When similar exploits show different impacts → highest, most irreversible impact used for scoring

---

## Platform-Specific Rules

### Centralization Risk
- All privileged roles are ASSUMED to be trustworthy
- Reckless admin mistakes → INVALID
- Direct misuse of privileges → QA report only
- Mistakes in code only reachable through admin mistakes → QA only
- Privilege escalation → judged by likelihood and impact, up to Medium