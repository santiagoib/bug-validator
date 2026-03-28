#!/usr/bin/env node

const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs");
const path = require("path");
const readline = require("readline");

// ── Paths ──
const SKILL_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE,
  ".claude",
  "skills",
  "bug-validator"
);
const ASCII_ART_PATH = path.join(SKILL_DIR, "ascii-art.txt");
const SKILL_PATH = path.join(SKILL_DIR, "SKILL.md");
const CRITERIA_PATH = path.join(SKILL_DIR, "criteria.md");

// ── Display ASCII art ──
function showBanner() {
  if (fs.existsSync(ASCII_ART_PATH)) {
    console.log(fs.readFileSync(ASCII_ART_PATH, "utf8"));
  }
  console.log("         Code4rena Acceptance Predictor — by mettal\n");
}

// ── Ask for file path ──
function askForFile() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(
      "Which .md report file should I validate?\nEnter the path (e.g. ./audit/report.md): ",
      (answer) => {
        rl.close();
        resolve(answer.trim());
      }
    );
  });
}

// ── Build system prompt ──
function buildSystemPrompt() {
  const skill = fs.existsSync(SKILL_PATH)
    ? fs.readFileSync(SKILL_PATH, "utf8")
    : "";
  const criteria = fs.existsSync(CRITERIA_PATH)
    ? fs.readFileSync(CRITERIA_PATH, "utf8")
    : "";

  return `You are Bug Validator — a Code4rena acceptance predictor for smart contract audit findings.

Your job is to analyze every finding in the provided audit report and predict whether a real C4 judge would accept it.

Follow this pipeline for each finding:

PHASE 1 — Automatic Invalidator Scan (check all AI-1 through AI-13 rules)
PHASE 2 — Severity Alignment Check (claimed vs actual C4 severity)
PHASE 3 — Quality Signal Assessment (root cause, impact, PoC, remediation)
PHASE 4 — Score Calculation (0-100%) and Verdict

Verdict thresholds:
- 70%+ → LIKELY VALID ✅
- 40-69% → BORDERLINE ⚠️
- <40% → LIKELY REJECTED ❌

${criteria ? "--- CRITERIA ---\n" + criteria : ""}

${skill ? "--- SKILL INSTRUCTIONS ---\n" + skill : ""}

OUTPUT FORMAT — write a complete Validation-Report.md with:
1. A summary table of all findings with scores and verdicts
2. Detailed analysis per finding including:
   - Automatic invalidators triggered (if any)
   - Severity assessment
   - Quality signals table
   - What's hurting the finding
   - What's strengthening the finding
   - How to improve it

Be strict and calibrated. Never score above 95%. Your role is the judge's internal monologue, not the warden's advocate.`;
}

// ── Stream response and write output ──
async function run() {
  showBanner();

  // Allow path as CLI argument or prompt
  let reportPath = process.argv[2];
  if (!reportPath) {
    reportPath = await askForFile();
  }

  if (!fs.existsSync(reportPath)) {
    console.error(`\n❌ File not found: ${reportPath}`);
    process.exit(1);
  }

  const reportContent = fs.readFileSync(reportPath, "utf8");
  const reportDir = path.dirname(path.resolve(reportPath));
  const outputPath = path.join(reportDir, "Validation-Report.md");

  console.log(`\n🔍 Analyzing findings in: ${reportPath}`);
  console.log("⏳ Running validation pipeline...\n");

  const client = new Anthropic();

  let fullResponse = "";

  process.stdout.write("📝 ");

  const stream = await client.messages.stream({
    model: "claude-sonnet-4-20250514",
    max_tokens: 8000,
    system: buildSystemPrompt(),
    messages: [
      {
        role: "user",
        content: `Please validate all findings in this audit report and produce a complete Validation-Report.md:\n\n${reportContent}`,
      },
    ],
  });

  for await (const chunk of stream) {
    if (
      chunk.type === "content_block_delta" &&
      chunk.delta.type === "text_delta"
    ) {
      fullResponse += chunk.delta.text;
      process.stdout.write(".");
    }
  }

  console.log("\n");

  // Write output file
  const header = `# Bug Validator — Validation Report\n\n**Input report**: ${path.basename(reportPath)}\n**Date**: ${new Date().toISOString().split("T")[0]}\n\n---\n\n`;
  fs.writeFileSync(outputPath, header + fullResponse, "utf8");

  // Count verdicts
  const valid = (fullResponse.match(/LIKELY VALID/g) || []).length;
  const borderline = (fullResponse.match(/BORDERLINE/g) || []).length;
  const rejected = (fullResponse.match(/LIKELY REJECTED/g) || []).length;
  const total = valid + borderline + rejected;

  console.log(`✅ Validation complete. Report saved to: ${outputPath}`);
  console.log(
    `   ${total} findings analyzed — ${valid} likely valid, ${borderline} borderline, ${rejected} likely rejected.\n`
  );
}

run().catch((err) => {
  console.error("\n❌ Error:", err.message);
  process.exit(1);
});
