# Changelog

All notable changes to Bug Validator will be documented in this file.
---

## [2.0.0] — 2026-03-30

### Added
- **Multi-platform support**: Competitive audits (Code4rena, Sherlock, Cantina, HackenProof) and bug bounties (Immunefi, Sherlock, Cantina, HackenProof).
- **Platform-specific criteria files**: `criteria-sherlock.md`, `criteria-cantina.md`, `criteria-bb.md`, `criteria-bb-cantina.md` in `references/`.
- **Criteria-driven output**: Every piece of feedback in the validation report now cites specific rules (AI-IDs, severity definitions, PoC requirements) from the loaded platform criteria.
- **Reasoning section** in detailed results: 4-8 sentence analysis thinking through acceptance probability as a judge would.
- **Score Breakdown** section: Transparent deduction-by-deduction view of how the final score was calculated.
- **Version tracking**: Version number in SKILL.md frontmatter, output banner, and validation reports.
- This CHANGELOG.

### Changed
- **Scoring model**: Switched from additive (base 50, add/subtract) to subtractive (start at 100, deduct for issues). Scores are now X/100 instead of X%.
- **Severity alignment**: Now platform-aware. Sherlock's H/M-only model, Cantina's Impact x Likelihood matrix, and Immunefi's 4-level impact lists are each applied correctly.
- **PoC assessment**: Platform-specific weight. Mandatory PoC platforms (Immunefi, HackenProof) apply an additional -25 penalty when PoC is missing.
- **"What's Hurting / Strengthening" sections** replaced by the more actionable "Reasoning" and "How to Improve Before Submission" sections.
- Banner text updated from "Code4rena Acceptance Predictor" to "Smart Contract Finding Validator".

### Removed
- Verification status parsing (CONFIRMED / CONTESTED / UNVERIFIED). Was not used in the pipeline and added unnecessary token consumption.




