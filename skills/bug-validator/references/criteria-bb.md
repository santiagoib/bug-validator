# Bug Bounty — Judging Criteria

Unified criteria for Immunefi, Sherlock Bug Bounty, and HackenProof.
Built from the superset of rules across all three platforms.

Sources:
- https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3/
- https://docs.sherlock.xyz/bug-bounties/criteria-for-bug-bounty-reports-validity
- https://docs.hackenproof.com/bug-bounty/vulnerability-classification/smart-contracts

---

## Severity Definitions

| Level | Impacts |
|-------|---------|
| **Critical** | Direct theft of user funds (at-rest or in-motion); Direct theft of NFTs; Permanent freezing of funds/NFTs; Unauthorized minting/burning of tokens; Governance result manipulation with direct outcome change (vote hijacking, quorum bypass); Protocol insolvency (under-collateralization, unbacked tokens, critical mispricing); Unintended alteration of NFT representation |
| **High** | Theft of unclaimed yield/royalties; Permanent freezing of unclaimed yield/royalties; Temporary freezing of funds/NFTs; Oracle manipulation (influencing on-chain price feeds) |
| **Medium** | Smart contract unable to operate due to lack of token funds; Block stuffing; Griefing (no profit motive, but damage to protocol/users); Theft of gas; Unbounded gas consumption; Gas limit/Out-of-Gas vulnerabilities; Denial of Service (gas exhaustion, malicious state manipulation) |
| **Low** | Contract fails to deliver promised returns but does not lose value; Uninitialized storage variables (potential privilege escalation but frequently low-risk) |

If the issue does not fit any category, CVSS can be used as a fallback to determine severity.

---

## Automatic Invalidators (AI)

| ID | Rule | Result |
|----|------|--------|
| AI-1 | Exploit requires the reporter to have already exploited it causing damage | INVALID |
| AI-2 | Requires access to leaked keys/credentials | INVALID |
| AI-3 | Requires access to privileged addresses (admin/owner) without additional modifications to privileges | INVALID |
| AI-4 | External stablecoin depeg without the attacker directly causing the depeg through a code bug | INVALID |
| AI-5 | Secrets/API keys/private keys on Github without proof of production use | INVALID |
| AI-6 | Best practice recommendations without concrete impact | INVALID |
| AI-7 | Feature requests | INVALID |
| AI-8 | Incorrect data from third-party oracles (does not exclude oracle manipulation/flash loan attacks) | INVALID |
| AI-9 | Basic economic/governance attacks (e.g. 51% attack) | INVALID |
| AI-10 | Lack of liquidity impacts | INVALID |
| AI-11 | Sybil attack impacts | INVALID |
| AI-12 | Centralization risks | INVALID |
| AI-13 | Gas optimizations | INVALID |
| AI-14 | Incorrect values in emitted events | INVALID |
| AI-15 | Zero address checks | INVALID |
| AI-16 | User input validation to prevent user mistakes (unless it causes significant loss to others) | INVALID |
| AI-17 | Admin incorrect call order (e.g. forgot to call setWithdrawAddress before withdrawAll) | INVALID |
| AI-18 | Admin action that breaks code assumptions (e.g. pausing collateral causes liquidations) | INVALID |
| AI-19 | Contract/Admin blacklisting affects protocol functionality | INVALID |
| AI-20 | Front-running initializers without irreversible damage or fund loss | INVALID |
| AI-21 | User experience issues without fund loss | INVALID |
| AI-22 | User blacklisted by token causing damage only to themselves | INVALID |
| AI-23 | Future opcode gas repricing | INVALID |
| AI-24 | Accidental direct token transfer that only damages the user | INVALID |
| AI-25 | Loss of airdrops/rewards not part of the original design | INVALID |
| AI-26 | Incorrect values in view functions (unless they feed functions that handle funds with real loss) | INVALID |
| AI-27 | Stale prices / Chainlink round completeness (except pull-based oracles like Pyth) | INVALID |
| AI-28 | Findings from previous audits marked as acknowledged/wontfix | INVALID |
| AI-29 | Chain re-org / network liveness (unless the attacker can force a chain re-org affecting the protocol) | INVALID |
| AI-30 | ERC721 unsafe mint (user cannot safemint due to unsupported implementation) | INVALID |
| AI-31 | Future issues from integrations not mentioned in the program | INVALID |
| AI-32 | Non-standard/weird tokens (unless explicitly mentioned in the program). Tokens with 6-18 decimals are NOT weird | INVALID |
| AI-33 | EVM opcodes incompatible with the network (manageable with compilation flags) | INVALID |
| AI-34 | Sequencer downtime/misbehavior | INVALID |
| AI-35 | Design decisions without fund loss | INVALID |
| AI-36 | Lack of storage gaps in parent contracts (simple) | INVALID |
| AI-37 | Theoretical vulnerabilities without proof or impact demonstration | INVALID |

---

## PoC Requirements

**PoC is MANDATORY for all severities.**

Without a PoC → finding will not be considered valid, regardless of technical merit.

The PoC must:
- Compile and execute successfully
- Demonstrate concrete impact (not just prove a function can be called)
- Use realistic conditions (do not assume arbitrary balances or impossible states)

---

## Quality Signals

What triagers look for when evaluating a finding:

| Signal | Full Credit | Partial Credit / Downgrade | Invalidation Risk |
|--------|------------|---------------------------|-------------------|
| PoC | Compiles, executes, demonstrates real impact with realistic conditions | Compiles but uses unrealistic setup or doesn't show full impact | Critical — no PoC = automatic rejection |
| Root cause | Clearly identified in the in-scope code | Symptom described but root cause unclear | High — theoretical findings rejected (AI-37) |
| Impact demonstration | Concrete numbers showing economic damage (theft amount, frozen funds, etc.) | Impact claimed but not quantified | High — must match severity level impacts |
| Severity alignment | Impact matches the specific impact list for the claimed level | Impact exists but at a lower level | High — triagers enforce impact lists strictly |
| Attack path | Step-by-step from root cause to exploit with realistic conditions | Partial path or unrealistic conditions | Moderate — weakens credibility |
| Remediation | Present and correct | Wrong or missing | Low — does not invalidate but helps credibility |

Key emphasis for bug bounties:
- The PoC is everything. A perfect writeup without a PoC will be rejected.
- Match your impact to the EXACT impact list for the severity level you're claiming. "Direct theft of funds" is Critical. "Theft of unclaimed yield" is High. Don't confuse them.
- Each program can override these defaults. Always check the program-specific scope and impact list before submitting.

---

## Source of Truth

Each bug bounty program defines its own list of in-scope and out-of-scope impacts that can override the defaults above. The Bug Bounty Page / specific program is the primary source of truth, above the defaults in this guide.

Always check:
- Which assets are in-scope
- Which impacts the program accepts
- Whether there are additional restrictions (e.g. Critical/High only, or specific exclusions)

---

## Scope

- If a contract is in-scope, all its parent contracts are included
- Vulnerability in a library used by an in-scope contract → valid
- Contract out of scope → INVALID

---

## Duplicate Rules

Duplicates are determined by root cause: if two findings share the same root cause or vulnerability even if they appear in different contracts → duplicates.

On platforms with first-come-first-served (like Sherlock BB), only the first submission (by timestamp) is rewarded. On Immunefi, the first reporter also has priority.

---

## Platform-Specific Rules

### Immunefi — Program Primacy
Each Immunefi program can define its own severity levels and impact lists that override the defaults above. Some programs only accept Critical/High. Always review the specific program page before submitting.

### Sherlock BB — Timestamp Priority
Duplicates are NOT rewarded. The first submission (by timestamp) wins. The Bug Bounty Page (not the README) is the source of truth.

### HackenProof — Reputation and Paid Submissions
Some HackenProof programs require minimum reputation points to submit. Certain programs use paid submissions (fee per report). Top 100 researchers may receive special consideration.