#!/bin/bash

set -e

COMMANDS_DIR="$HOME/.claude/commands"
SKILLS_DIR="$HOME/.claude/skills/bug-validator"
CLAUDE_DIR="$HOME/.claude"

echo ""
echo "Installing Bug Validator v2.0.0..."
echo ""

# ── Claude Code skill ──
mkdir -p "$COMMANDS_DIR" "$SKILLS_DIR/references"
cp commands/bug-validator.md "$COMMANDS_DIR/bug-validator.md"
cp skills/bug-validator/SKILL.md "$SKILLS_DIR/SKILL.md"
cp skills/bug-validator/references/* "$SKILLS_DIR/references/"
echo "✅ Claude Code skill installed → /bug-validator"

# ── Python wrapper ──
cp bug-validator.py "$CLAUDE_DIR/bug-validator.py"
chmod +x "$CLAUDE_DIR/bug-validator.py"

# ── PATH entry (add to ~/.bashrc and ~/.zshrc if not already there) ──
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ] && ! grep -q "bug-validator" "$rc"; then
        echo "" >> "$rc"
        echo "# Bug Validator" >> "$rc"
        echo "alias bug-validator='python3 $CLAUDE_DIR/bug-validator.py'" >> "$rc"
    fi
done

echo "✅ CLI installed → bug-validator"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Usage:"
echo ""
echo "  Option 1 — terminal (anywhere)"
echo "    bug-validator                      ← prompts for file"
echo "    bug-validator ./audit/report.md    ← direct path"
echo ""
echo "  Option 2 — Claude Code skill"
echo "    claude  →  /bug-validator"
echo ""
echo "  Reload your shell to activate the alias:"
echo "    source ~/.bashrc   (or ~/.zshrc)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""