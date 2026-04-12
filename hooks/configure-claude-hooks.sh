#!/bin/bash
# Configure Claude Code hooks for Tivoo pixel screen notifications
# Uses Claude emotion presets (--load claude) by default.
#
# Usage:
#   ./configure-claude-hooks.sh                    # Apply default hooks (English TTS)
#   ./configure-claude-hooks.sh -l zh              # Chinese TTS for Notification
#   ./configure-claude-hooks.sh --all              # Enable all hooks
#   ./configure-claude-hooks.sh --dry-run          # Print config without applying
#   ./configure-claude-hooks.sh --events Stop,Notification  # Only these events
#   ./configure-claude-hooks.sh --tts Stop,StopFailure      # TTS for extra events
#   ./configure-claude-hooks.sh --no-tts           # Disable all TTS
#   ./configure-claude-hooks.sh --no-load          # Use generic presets instead
#   ./configure-claude-hooks.sh --reset            # Remove all Tivoo hooks
#
# Requires: jq, python3, tivoo_macos.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIVOO_DIR="$(dirname "$SCRIPT_DIR")"
TIVOO_PY="$TIVOO_DIR/tivoo_macos.py"
SETTINGS_FILE="$HOME/.claude/settings.json"

# ── Event → Preset mapping ──────────────────────────────────────────
# Format: EVENT:PRESET:LOOP:TTS_CN:TTS_EN:DEFAULT
# DEFAULT=1 means enabled by default, 0 means opt-in only
# TTS only on Notification by default — other events use emotion only
HOOK_MAP=(
  # Needs user attention (default enabled)
  "Stop:done:5:::1"
  "StopFailure:oops:5:::1"
  "Notification:notify:5:通知来啦:Heads up:1"
  "PermissionRequest:question:5:::1"
  "Elicitation:question:5:::1"
  "TeammateIdle:standby:5:::1"
  # Progress feedback (opt-in)
  "UserPromptSubmit:working:2:::1"
  "TaskCreated:tasklist:2:::0"
  "TaskCompleted:taskdone:2:::0"
  "SubagentStart:subagent:2:::0"
  "SubagentStop:taskdone:2:::0"
  # Errors (opt-in)
  "PostToolUseFailure:oops:2:::0"
  "PermissionDenied:oops:2:::0"
)

# ── Parse arguments ──────────────────────────────────────────────────
DRY_RUN=false
NO_LOAD=false
RESET=false
ALL_EVENTS=false
NO_TTS=false
LANG="en"
FILTER_EVENTS=""
TTS_EVENTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)   DRY_RUN=true; shift ;;
    --no-load)   NO_LOAD=true; shift ;;
    --reset)     RESET=true; shift ;;
    --all)       ALL_EVENTS=true; shift ;;
    --no-tts)    NO_TTS=true; shift ;;
    --lang|-l)   LANG="$2"; shift 2 ;;
    --events)    FILTER_EVENTS="$2"; shift 2 ;;
    --tts)       TTS_EVENTS="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^$/s/^# //p' "$0"
      echo ""
      echo "Events and presets:"
      for entry in "${HOOK_MAP[@]}"; do
        IFS=: read -r ev preset loop tts_cn tts_en def <<< "$entry"
        dflag=$([[ "$def" == "1" ]] && echo "*" || echo " ")
        tts_display=""
        if [[ -n "$tts_cn" ]]; then
          tts_display="  tts: $tts_cn / $tts_en"
        fi
        printf "  %s %-22s → %-12s loop=%-2s%s\n" "$dflag" "$ev" "$preset" "$loop" "$tts_display"
      done
      echo ""
      echo "  * = enabled by default"
      echo ""
      echo "Options:"
      echo "  -l, --lang en|zh  TTS language (default: en)"
      echo "  --dry-run       Print config without applying"
      echo "  --all           Enable all events"
      echo "  --events E,...  Enable only listed events"
      echo "  --tts E,...     TTS for extra events (Notification always has TTS)"
      echo "  --no-tts        Disable all TTS"
      echo "  --no-load       Use generic presets instead of Claude emotions"
      echo "  --reset         Remove all Tivoo hooks"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Normalize zh → cn
if [[ "$LANG" == "zh" ]]; then
  LANG="cn"
fi

# Validate --lang
if [[ "$LANG" != "cn" && "$LANG" != "en" ]]; then
  echo "Error: -l/--lang must be 'en' or 'zh'"
  exit 1
fi

# TTS voice per language
if [[ "$LANG" == "cn" ]]; then
  TTS_VOICE="Tingting"
else
  TTS_VOICE="Samantha"
fi

# ── Reset mode ───────────────────────────────────────────────────────
if $RESET; then
  if [[ ! -f "$SETTINGS_FILE" ]]; then
    echo "No settings file found at $SETTINGS_FILE"
    exit 0
  fi
  RESULT=$(jq 'del(.hooks)' "$SETTINGS_FILE")
  if $DRY_RUN; then
    echo "$RESULT"
  else
    echo "$RESULT" > "$SETTINGS_FILE"
    echo "Removed all hooks from $SETTINGS_FILE"
  fi
  exit 0
fi

# ── Check dependencies ───────────────────────────────────────────────
if ! command -v jq &>/dev/null; then
  echo "Error: jq is required. Install with: brew install jq"
  exit 1
fi
if [[ ! -f "$TIVOO_PY" ]]; then
  echo "Error: tivoo_macos.py not found at $TIVOO_PY"
  exit 1
fi

# ── Helper: check if event is in comma-separated list ────────────────
in_list() {
  local item="$1" list="$2"
  IFS=',' read -ra arr <<< "$list"
  for e in "${arr[@]}"; do
    [[ "$e" == "$item" ]] && return 0
  done
  return 1
}

# ── Build hook shell scripts ─────────────────────────────────────────
HOOKS_DIR="$SCRIPT_DIR/generated-claude"
mkdir -p "$HOOKS_DIR"

HOOKS_JSON='{}'

# Default: --load claude (Claude emotions)
LOAD_FLAG=" --load claude"
if $NO_LOAD; then
  LOAD_FLAG=""
fi

for entry in "${HOOK_MAP[@]}"; do
  IFS=: read -r EVENT PRESET LOOP TTS_CN TTS_EN DEFAULT <<< "$entry"

  # Filter: if --events specified, only include those
  if [[ -n "$FILTER_EVENTS" ]]; then
    in_list "$EVENT" "$FILTER_EVENTS" || continue
  elif ! $ALL_EVENTS && [[ "$DEFAULT" != "1" ]]; then
    continue
  fi

  # Select TTS text by language
  if [[ "$LANG" == "cn" ]]; then
    TTS_TEXT="$TTS_CN"
  else
    TTS_TEXT="$TTS_EN"
  fi

  RESTORE_CMD="preset standby --loop 20$LOAD_FLAG"
  PRESET_CMD="python3 $TIVOO_PY preset $PRESET --loop $LOOP$LOAD_FLAG --restore '$RESTORE_CMD'"

  # Check if TTS is applicable
  WANT_TTS=false
  if ! $NO_TTS && [[ -n "$TTS_TEXT" ]]; then
    if [[ -n "$TTS_EVENTS" ]]; then
      in_list "$EVENT" "$TTS_EVENTS" && WANT_TTS=true
    else
      WANT_TTS=true
    fi
  fi

  # Write individual hook script
  EVENT_LOWER=$(echo "$EVENT" | tr '[:upper:]' '[:lower:]')
  HOOK_SCRIPT="$HOOKS_DIR/on-${EVENT_LOWER}.sh"

  # Common header: shebang + comment + logging
  cat > "$HOOK_SCRIPT" << 'HOOKEOF'
#!/bin/bash
HOOKEOF
  cat >> "$HOOK_SCRIPT" << HOOKEOF
# Tivoo hook: $EVENT → $PRESET (loop $LOOP)
# Auto-generated by configure-claude-hooks.sh
HOOKEOF
  cat >> "$HOOK_SCRIPT" << 'HOOKEOF'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/hooks.log"
INPUT=$(cat)

# Log hook input
{
  echo "--- $(date '+%Y-%m-%d %H:%M:%S') $0 ---"
  echo "$INPUT"
  echo ""
} >> "$LOG_FILE"

HOOKEOF

  # Event-specific body — all background processes fully detached
  if [[ "$EVENT" == "Notification" ]]; then
    # Notification: read message from JSON input and speak it
    cat >> "$HOOK_SCRIPT" << HOOKEOF
$PRESET_CMD </dev/null >/dev/null 2>&1 &
HOOKEOF
    if $WANT_TTS; then
      cat >> "$HOOK_SCRIPT" << 'HOOKEOF'

# Extract notification message and speak it
MSG=$(echo "$INPUT" | jq -r '.message // .title // .text // empty' 2>/dev/null)
HOOKEOF
      cat >> "$HOOK_SCRIPT" << HOOKEOF
(
  if [[ -n "\$MSG" ]]; then
    say -v $TTS_VOICE "$TTS_TEXT" 2>/dev/null
    say -v $TTS_VOICE "\$MSG" 2>/dev/null
  else
    say -v $TTS_VOICE "$TTS_TEXT" 2>/dev/null
  fi
) </dev/null >/dev/null 2>&1 &
HOOKEOF
    fi

  else
    # Standard: preset with restore, fully detached
    cat >> "$HOOK_SCRIPT" << HOOKEOF
$PRESET_CMD </dev/null >/dev/null 2>&1 &
HOOKEOF
    if $WANT_TTS; then
      cat >> "$HOOK_SCRIPT" << HOOKEOF
say -v $TTS_VOICE "$TTS_TEXT" </dev/null >/dev/null 2>&1 &
HOOKEOF
    fi
  fi

  cat >> "$HOOK_SCRIPT" << 'HOOKEOF'

exit 0
HOOKEOF
  chmod +x "$HOOK_SCRIPT"

  # Build JSON entry for this event
  HOOK_ENTRY=$(jq -n --arg cmd "$HOOK_SCRIPT" \
    '[{"hooks": [{"type": "command", "command": $cmd}]}]')

  HOOKS_JSON=$(echo "$HOOKS_JSON" | jq --arg event "$EVENT" --argjson entry "$HOOK_ENTRY" \
    '. + {($event): $entry}')
done

# ── Merge into settings.json ─────────────────────────────────────────
if [[ ! -f "$SETTINGS_FILE" ]]; then
  mkdir -p "$(dirname "$SETTINGS_FILE")"
  echo '{}' > "$SETTINGS_FILE"
fi

EXISTING=$(cat "$SETTINGS_FILE")
RESULT=$(echo "$EXISTING" | jq --argjson hooks "$HOOKS_JSON" '.hooks = $hooks')

if $DRY_RUN; then
  echo "=== Generated hook scripts in $HOOKS_DIR ==="
  ls -1 "$HOOKS_DIR"/on-*.sh 2>/dev/null || echo "(none)"
  echo ""
  echo "=== Settings JSON ==="
  echo "$RESULT" | jq .
else
  echo "$RESULT" > "$SETTINGS_FILE"

  # Count enabled hooks
  COUNT=$(echo "$HOOKS_JSON" | jq 'length')
  echo "Configured $COUNT Claude Code hooks ($LANG) in $SETTINGS_FILE"
  echo "Hook scripts in $HOOKS_DIR/"
  echo ""
  echo "Enabled events:"
  echo "$HOOKS_JSON" | jq -r 'keys[]' | while read -r ev; do
    echo "  - $ev"
  done
fi
