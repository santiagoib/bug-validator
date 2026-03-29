# Code4rena Judging Criteria - Codified

Source: https://docs.code4rena.com/competitions/judging-criteria
Source: https://docs.code4rena.com/competitions/severity-categorization

---

## AUTOMATIC INVALIDATORS
These are hard rules. If any applies, the finding is invalid or capped regardless of technical merit.

| ID  | Rule | Result |
|-----|------|--------|
| AI-1 | Root cause is in an out-of-scope library/contract (not in how the in-scope contract uses it) | INVALID - OOS |
| AI-2 | Finding requires the user to make a mistake or enter wrong input | INVALID or QA at best |
| AI-3 | Non-standard / weird ERC-20 token or fee-on-transfer token, unless explicitly listed as supported in scope (USDT is always in scope) | INVALID |
| AI-4 | Admin/owner direct misuse of privileges (reckless admin mistake) | QA only - not Medium/High |
| AI-5 | Approve / safeApprove front-run race condition | INVALID |
| AI-6 | Unused view function finding | QA/Low only |
| AI-7 | Faulty event emission with no broader on-chain impact | Capped Low |
| AI-8 | Speculation on future code not in scope | INVALID unless root cause is demonstrably in scope |
| AI-9 | Loss of dust only (rounding errors, marginal fee variations) | QA/Low only |
| AI-10 | Loss of unmatured yield or yield in motion | Capped Medium |
| AI-11 | Finding published in a prior audit report listed in README (acknowledged/wontfix) | OOS / Known issue |
| AI-12 | CryptoPunks non-support | INVALID - Informational only |
| AI-13 | Phishing or improper user caution | INVALID |

---

## SEVERITY RULES

### High (3)
- Assets (funds, NFTs, data, authorization) can be stolen/lost/compromised DIRECTLY
- OR indirectly, but ONLY with a valid attack path - no hand-wavy hypotheticals
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

## QUALITY SIGNAL CHECKLIST

### Required for full credit:
- Root cause clearly identified
- Maximum achievable impact demonstrated
- Step-by-step explanation from root cause to impact OR coded PoC
- Code snippets attached
- Remediation steps present and correct
- Severity matches actual impact per C4 definitions

### Grounds for partial credit / downgrade:
- Root cause missing or unclear → partial scoring or invalidation
- Maximal impact not identified → partial scoring or downgrade
- PoC does not pass burden of proof → insufficient quality
- Severity clearly inflated → may be deemed insufficient quality
- Low/incomplete effort → insufficient quality

### Grounds for invalidation despite technical validity:
- Does not add value to the sponsor
- Appears to be a direct copy of another report in the same audit

---

## DUPLICATE RULES
- Findings are duplicates if they share the same ROOT CAUSE
- Fixing the root cause would make both unexploitable
- When similar exploits show different impacts → highest, most irreversible impact used for scoring

---

## CENTRALIZATION RISK RULES
- All privileged roles are ASSUMED to be trustworthy
- Reckless admin mistakes → INVALID
- Direct misuse of privileges → QA report only
- Mistakes in code only reachable through admin mistakes → QA only
- Privilege escalation → judged by likelihood and impact, up to Medium

---

## OUT-OF-SCOPE LIBRARY RULES
- Root cause IN the OOS library → finding is OOS (invalid)
- Root cause in how the IN-SCOPE contract incorrectly uses the OOS library → VALID finding
