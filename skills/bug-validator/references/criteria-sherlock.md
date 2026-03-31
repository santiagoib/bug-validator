# Sherlock Competitive — Judging Criteria

Source: https://docs.sherlock.xyz/audits/judging/guidelines

---

## Severity Definitions

Sherlock ONLY accepts High and Medium. Low and Informational are NOT rewarded. If the finding is Low or Informational → INVALID for Sherlock.

### High
- Direct fund loss WITHOUT extensive external conditions
- The loss must be SIGNIFICANT:
  - Users lose >1% AND >$10 of their principal
  - Users lose >1% AND >$10 of their yield
  - The protocol loses >1% AND >$10 of fees

### Medium
- Fund loss that requires external conditions or specific states
- OR breaks CORE contract functionality
- The loss must be RELEVANT:
  - Users lose >0.01% AND >$10 of their principal
  - Users lose >0.01% AND >$10 of their yield
  - The protocol loses >0.01% AND >$10 of fees
- Note: if the attack can be repeated indefinitely with 0.01% loss per iteration → consider 100% loss

### DOS Severity
- DOS valid as Medium if: funds locked >1 week OR time-sensitive function affected
- DOS valid as High if: both conditions above apply
- DOS of <1 week → evaluate as single occurrence; only valid if it affects a clearly time-sensitive function

**IMPORTANT: Likelihood is NOT considered when determining severity in Sherlock. Only impact matters.**

---

## Automatic Invalidators (AI)

| ID | Rule | Result |
|----|------|--------|
| AI-1 | Severity is Low or Informational | INVALID — Sherlock only pays H/M |
| AI-2 | Gas optimization without fund loss | INVALID |
| AI-3 | Event emitted with incorrect value (no on-chain impact) | INVALID |
| AI-4 | Zero address check | INVALID |
| AI-5 | User input validation without significant loss to others | INVALID |
| AI-6 | Admin incorrect call order (e.g. forgot to call setWithdrawAddress before withdrawAll) | INVALID |
| AI-7 | Admin action that breaks assumptions (e.g. pausing collateral causes liquidations) | INVALID |
| AI-8 | Contract/Admin address blacklisting affects functionality | INVALID |
| AI-9 | Front-running initializers without irreversible damage or fund loss | INVALID |
| AI-10 | User experience issue without fund loss | INVALID |
| AI-11 | User blacklisted by token causing damage only to themselves | INVALID |
| AI-12 | Future opcode gas repricing | INVALID |
| AI-13 | Accidental direct token transfer that only damages the user themselves | INVALID |
| AI-14 | Loss of airdrops or rewards not part of the original design | INVALID |
| AI-15 | Incorrect values in view functions (no impact on functions that handle funds) | INVALID — Low in Sherlock |
| AI-16 | Stale prices / Chainlink round completeness (except pull-based oracles like Pyth) | INVALID |
| AI-17 | Finding in previous audit marked as acknowledged/wontfix | INVALID |
| AI-18 | Chain re-org / network liveness | INVALID |
| AI-19 | ERC721 unsafe mint (user cannot safemint due to unsupported implementation) | INVALID |
| AI-20 | Future issues from integrations not mentioned in docs/README | INVALID |
| AI-21 | Non-standard/weird ERC20 tokens (unless explicitly mentioned in README). Tokens with 6-18 decimals are NOT weird | INVALID |
| AI-22 | EVM opcodes that don't work on the protocol's network | INVALID |
| AI-23 | Sequencer downtime/misbehavior | INVALID |
| AI-24 | Design decision without fund loss | INVALID — Informational |
| AI-25 | Storage gaps in parent contracts (simple) | INVALID — Low |
| AI-26 | Front-running on chain with private mempool (e.g. Optimism) without explaining unintentional front-run | Downgrade: H→M, M→INVALID |
| AI-27 | Approval/ERC20 race condition | INVALID |

---

## PoC Requirements

PoC is recommended but not mandatory on Sherlock. However, it is strongly recommended for:
- Vulnerabilities with complex attack paths
- Non-trivial input constraints
- Precision loss
- Reentrancy
- Gas consumption / reverting calls

If the finding does NOT include a PoC and CANNOT be clearly understood without one → INVALID.

---

## Quality Signals

What judges look for when evaluating a finding:

| Signal | Full Credit | Partial Credit / Downgrade | Invalidation Risk |
|--------|------------|---------------------------|-------------------|
| Root cause | Clearly identified in the in-scope code | Symptom described but root cause unclear | High — may invalidate |
| Loss quantification | Concrete math showing loss exceeds severity thresholds (>1%/$10 for High, >0.01%/$10 for Medium) | Loss claimed but not quantified | High — judges enforce thresholds strictly |
| Attack path | Step-by-step from root cause to fund loss, or coded PoC | Partial path, missing steps | Moderate — weakens finding significantly |
| External conditions | Clearly stated and realistic | Unrealistic or unstated assumptions | High — extensive conditions downgrade H→M |
| Remediation | Present and correct | Wrong or missing | Low — does not invalidate but loses credit |
| Severity alignment | Matches Sherlock definitions (only H/M valid) | Finding is actually Low/Informational | Critical — automatic invalidation |

Key emphasis for Sherlock:
- Quantify the loss with real numbers. Judges will check if the loss exceeds the defined thresholds.
- Clearly distinguish between "no external conditions" (High) vs "requires external conditions" (Medium).
- If the attack is repeatable, state so explicitly. Repeatable 0.01% loss = 100% loss = potentially High.

---

## Source of Truth

1. README (primary source)
2. Code comments (can be overridden by the judge if outdated)
3. Default guidelines

Only the README can define protocol invariants. Issues that break README invariants can be Medium even if the impact is low/unknown.

---

## Scope

- If a contract is in-scope, all its parent contracts are included by default
- Vulnerability in a library used by an in-scope contract → valid
- Contract in the repo but out of scope → INVALID

---

## Duplicate Rules

- Findings are duplicates if they share the same root cause
- Fixing the root cause would make both unexploitable
- Duplicate grouping applies even across different contracts

---

## Platform-Specific Rules

### Admin Trust
- Admin functions assumed to be used correctly by default
- EXCEPTION: if the protocol defines explicit restrictions in the README about the admin, issues that bypass those restrictions may be valid
- If the admin UNKNOWINGLY causes issues → may be valid
- Internal protocol roles are trusted by default; only untrusted if the README explicitly specifies it OR the user can obtain the role without admin permission