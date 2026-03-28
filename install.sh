#!/bin/bash

set -e

COMMANDS_DIR="$HOME/.claude/commands"
SKILLS_DIR="$HOME/.claude/skills"
CLAUDE_DIR="$HOME/.claude"

echo ""
echo "Installing Bug Validator..."
echo ""

# ── Claude Code skill ──
mkdir -p "$COMMANDS_DIR" "$SKILLS_DIR/bug-validator"
cp commands/bug-validator.md "$COMMANDS_DIR/bug-validator.md"
cp skills/bug-validator/SKILL.md "$SKILLS_DIR/bug-validator/SKILL.md"
cp skills/bug-validator/criteria.md "$SKILLS_DIR/bug-validator/criteria.md"
cp skills/bug-validator/ascii-art.txt "$SKILLS_DIR/bug-validator/ascii-art.txt"
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
