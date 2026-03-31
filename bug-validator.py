#!/usr/bin/env python3
"""Bug Validator v2.0.0 — Smart Contract Finding Validator.

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
CYAN   = "\x1b[38;2;0;180;220m"

SKILL_DIR  = os.path.join(os.path.expanduser("~"), ".claude", "skills", "bug-validator")
ASCII_PATH = os.path.join(SKILL_DIR, "references", "ascii-art.txt")
SKILL_PATH = os.path.join(SKILL_DIR, "SKILL.md")
REFS_DIR   = os.path.join(SKILL_DIR, "references")

CRITERIA_MAP = {
    ("competitive", "code4rena"):    "criteria.md",
    ("competitive", "sherlock"):     "criteria-sherlock.md",
    ("competitive", "cantina"):      "criteria-cantina.md",
    ("competitive", "hackenproof"):  "criteria-bb.md",
    ("competitive", "other"):        "criteria.md",
    ("bounty", "immunefi"):          "criteria-bb.md",
    ("bounty", "sherlock"):          "criteria-bb.md",
    ("bounty", "cantina"):           "criteria-bb-cantina.md",
    ("bounty", "hackenproof"):       "criteria-bb.md",
    ("bounty", "other"):             "criteria-bb.md",
}

def show_banner():
    if os.path.isfile(ASCII_PATH):
        with open(ASCII_PATH, "r", encoding="utf-8") as f:
            print(f.read())
    print(f"         {BOLD}Smart Contract Finding Validator v2.0.0{RST} {GRAY}— by mettal{RST}\n")

def check_claude():
    if not shutil.which("claude"):
        print(f"{RED}✗ claude CLI not found.{RST}")
        sys.exit(1)

def ask_choice(prompt, options):
    """Display a lettered menu and return the selected value."""
    print(f"{BOLD}{prompt}{RST}")
    letters = "ABCDEFGHIJ"
    for i, (label, _) in enumerate(options):
        print(f"  {CYAN}[{letters[i]}]{RST} {label}")
    print()
    while True:
        choice = input("→ ").strip().upper()
        for i, (_, value) in enumerate(options):
            if choice == letters[i]:
                return value
        print(f"  {RED}Invalid choice. Enter a letter ({letters[0]}-{letters[len(options)-1]}).{RST}")

def select_mode_and_platform():
    """Ask user for mode and platform, return (mode, platform, criteria_filename, display names)."""
    mode = ask_choice("What are you working on?", [
        ("Competitive Audit", "competitive"),
        ("Bug Bounty", "bounty"),
    ])

    if mode == "competitive":
        mode_display = "Competitive Audit"
        platform = ask_choice("Which platform?", [
            ("Code4rena", "code4rena"),
            ("Sherlock", "sherlock"),
            ("Cantina", "cantina"),
            ("HackenProof", "hackenproof"),
            ("Other", "other"),
        ])
    else:
        mode_display = "Bug Bounty"
        platform = ask_choice("Which platform?", [
            ("Immunefi", "immunefi"),
            ("Sherlock", "sherlock"),
            ("Cantina", "cantina"),
            ("HackenProof", "hackenproof"),
            ("Other", "other"),
        ])

    platform_display = platform.capitalize()
    if platform == "code4rena":
        platform_display = "Code4rena"
    elif platform == "hackenproof":
        platform_display = "HackenProof"

    criteria_file = CRITERIA_MAP[(mode, platform)]
    return mode, platform, criteria_file, mode_display, platform_display

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

def build_prompt(report_content, output_path, criteria_file, mode_display, platform_display):
    skill = read_file(SKILL_PATH) if os.path.isfile(SKILL_PATH) else ""

    criteria_path = os.path.join(REFS_DIR, criteria_file)
    criteria = read_file(criteria_path) if os.path.isfile(criteria_path) else ""

    return f"""You are Bug Validator — a smart contract finding validator.

{skill}

The user has already selected:
- Mode: {mode_display}
- Platform: {platform_display}

Skip Steps 1-3 (banner, mode selection, criteria loading) — they are already done.
Start directly from Step 4 (ask for report file is also done — the report is provided below).
Proceed with Step 5 (parse findings) and continue through Step 7 (write output).

Here are the judging criteria for {platform_display} ({mode_display}):

{criteria}

The output file must be saved to: {output_path}

Now validate every finding in the following audit report and write the complete Validation-Report.md to the path above:

---

{report_content}
"""

def run():
    show_banner()
    check_claude()

    mode, platform, criteria_file, mode_display, platform_display = select_mode_and_platform()
    print(f"\n{GREEN}✓{RST} {BOLD}{platform_display}{RST} ({mode_display}) — loading criteria...\n")

    report_path    = get_report_path()
    report_content = read_file(report_path)
    output_path    = os.path.join(os.path.dirname(os.path.abspath(report_path)), "Validation-Report.md")

    print(f"\n{ORANGE}>{RST} Analyzing: {BOLD}{report_path}{RST}")
    print(f"{ORANGE}>{RST} Platform: {BOLD}{platform_display} ({mode_display}){RST}")
    print(f"{ORANGE}>{RST} Output: {BOLD}{output_path}{RST}\n")
    sys.stdout.flush()

    prompt = build_prompt(report_content, output_path, criteria_file, mode_display, platform_display)

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