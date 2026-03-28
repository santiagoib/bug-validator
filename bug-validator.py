#!/usr/bin/env python3
"""Bug Validator — Code4rena Acceptance Predictor.

Launches Claude Code interactively to validate audit findings.
No API key needed — uses your existing Claude Code subscription.
"""

import sys, os, shutil, subprocess, tempfile

if sys.platform == "win32":
    import io
    os.system("")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

RST    = "\x1b[0m"
BOLD   = "\x1b[1m"
GREEN  = "\x1b[38;2;0;200;80m"
ORANGE = "\x1b[38;2;255;140;66m"
RED    = "\x1b[38;2;200;60;60m"
GRAY   = "\x1b[38;2;120;120;120m"

SKILL_DIR     = os.path.join(os.path.expanduser("~"), ".claude", "skills", "bug-validator")
ASCII_PATH    = os.path.join(SKILL_DIR, "ascii-art.txt")
SKILL_PATH    = os.path.join(SKILL_DIR, "SKILL.md")
CRITERIA_PATH = os.path.join(SKILL_DIR, "criteria.md")

def show_banner():
    if os.path.isfile(ASCII_PATH):
        with open(ASCII_PATH, "r", encoding="utf-8") as f:
            print(f.read())
    print(f"         {BOLD}Code4rena Acceptance Predictor{RST} {GRAY}by mettal{RST}\n")

def check_claude():
    if not shutil.which("claude"):
        print(f"{RED}✗ claude CLI not found.{RST}")
        sys.exit(1)

def get_report_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    print(f"Which {BOLD}.md{RST} report file should I validate?")
    return input("Enter path (e.g. ./audit/report.md): ").strip()

def read_file(path):
    if not os.path.isfile(path):
        print(f"\n{RED}✗ File not found: {path}{RST}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(report_content, output_path):
    skill    = read_file(SKILL_PATH)    if os.path.isfile(SKILL_PATH)    else ""
    criteria = read_file(CRITERIA_PATH) if os.path.isfile(CRITERIA_PATH) else ""
    return f"""You are Bug Validator — a Code4rena acceptance predictor for smart contract audit findings.

{skill}

{criteria}

The output file must be saved to: {output_path}

Now validate every finding in the following audit report and write the complete Validation-Report.md to the path above:

---

{report_content}
"""

def run():
    show_banner()
    check_claude()

    report_path    = get_report_path()
    report_content = read_file(report_path)
    output_path    = os.path.join(os.path.dirname(os.path.abspath(report_path)), "Validation-Report.md")

    print(f"\n{ORANGE}>{RST} Analyzing: {BOLD}{report_path}{RST}")
    print(f"{ORANGE}>{RST} Output: {BOLD}{output_path}{RST}\n")
    sys.stdout.flush()

    prompt = build_prompt(report_content, output_path)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(prompt)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            subprocess.run(["claude"], stdin=f, text=True)
    except KeyboardInterrupt:
        print(f"\n{GRAY}Interrupted.{RST}")
    finally:
        os.unlink(tmp_path)

    if os.path.isfile(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        valid      = content.count("LIKELY VALID")
        borderline = content.count("BORDERLINE")
        rejected   = content.count("LIKELY REJECTED")
        total      = valid + borderline + rejected
        print(f"\n{GREEN}✅ Done. Report: {BOLD}{output_path}{RST}")
        if total > 0:
            print(f"   {total} findings — {GREEN}{valid} valid{RST}, {ORANGE}{borderline} borderline{RST}, {RED}{rejected} rejected{RST}\n")
    else:
        print(f"\n{ORANGE}⚠ Validation-Report.md not found — check output above.{RST}\n")

if __name__ == "__main__":
    run()
