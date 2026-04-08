#!/bin/bash
# Configure Claude Code hooks for Tivoo pixel screen notifications
#
# Usage:
#   ./configure-hooks.sh                    # Apply default hooks (Chinese TTS)
#   ./configure-hooks.sh --lang en          # Apply default hooks (English TTS)
#   ./configure-hooks.sh --all              # Enable all hooks
#   ./configure-hooks.sh --dry-run          # Print config without applying
#   ./configure-hooks.sh --events Stop,Notification  # Only these events
#   ./configure-hooks.sh --tts Stop,StopFailure      # TTS for these events
#   ./configure-hooks.sh --no-tts           # Disable all TTS
#   ./configure-hooks.sh --luna             # Use Luna emotion presets
#   ./configure-hooks.sh --reset            # Remove all Tivoo hooks
#
# Requires: jq, python3, tivoo_macos.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIVOO_DIR="$(dirname "$SCRIPT_DIR")"
TIVOO_PY="$TIVOO_DIR/tivoo_macos.py"
SETTINGS_FILE="$HOME/.claude/settings.json"
LUNA_PRESETS="$TIVOO_DIR/emotion_presets_luna.py"

# ── Event → Preset mapping ──────────────────────────────────────────
# Format: EVENT:PRESET:LOOP:TTS_CN:TTS_EN:DEFAULT
# DEFAULT=1 means enabled by default, 0 means opt-in only
HOOK_MAP=(
  # Needs user attention (default enabled)
  "Stop:success:3:完成啦，等待指示:Done, awaiting instructions:1"
  "StopFailure:error:3:出错了，快来看看:Error, come take a look:1"
  "Notification:notify:5:通知来啦:Heads up:1"
  "PermissionRequest:waiting:5:等待授权:Approval needed:1"
  "Elicitation:coding:5:等待输入:Input needed:1"
  "TeammateIdle:idle:5:队友闲置:Teammate idle:1"
  # Progress feedback (opt-in)
  "UserPromptSubmit:searching:2:::0"
  "TaskCreated:building:2:::0"
  "TaskCompleted:check:2:子任务完成:Task done:0"
  "SubagentStart:working:2:::0"
  "SubagentStop:check:2:::0"
  # Errors (opt-in)
  "PostToolUseFailure:cross:2:::0"
  "PermissionDenied:cross:2:::0"
)

# ── Parse arguments ──────────────────────────────────────────────────
DRY_RUN=false
USE_LUNA=false
RESET=false
ALL_EVENTS=false
NO_TTS=false
LANG="cn"
FILTER_EVENTS=""
TTS_EVENTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)  DRY_RUN=true; shift ;;
    --luna)     USE_LUNA=true; shift ;;
    --reset)    RESET=true; shift ;;
    --all)      ALL_EVENTS=true; shift ;;
    --no-tts)   NO_TTS=true; shift ;;
    --lang)     LANG="$2"; shift 2 ;;
    --events)   FILTER_EVENTS="$2"; shift 2 ;;
    --tts)      TTS_EVENTS="$2"; shift 2 ;;
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
      echo "  --lang cn|en    TTS language (default: cn)"
      echo "  --dry-run       Print config without applying"
      echo "  --all           Enable all events"
      echo "  --events E,...  Enable only listed events"
      echo "  --tts E,...     TTS only for listed events"
      echo "  --no-tts        Disable all TTS"
      echo "  --luna          Use Luna emotion presets"
      echo "  --reset         Remove all Tivoo hooks"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Validate --lang
if [[ "$LANG" != "cn" && "$LANG" != "en" ]]; then
  echo "Error: --lang must be 'cn' or 'en'"
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
HOOKS_DIR="$SCRIPT_DIR/generated"
mkdir -p "$HOOKS_DIR"

HOOKS_JSON='{}'

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

  # Build the shell command
  LOAD_FLAG=""
  if $USE_LUNA; then
    LOAD_FLAG=" --load $LUNA_PRESETS"
  fi

  CMD="python3 $TIVOO_PY preset $PRESET --loop $LOOP$LOAD_FLAG 2>/dev/null"

  # Add TTS if applicable
  WANT_TTS=false
  if ! $NO_TTS && [[ -n "$TTS_TEXT" ]]; then
    if [[ -n "$TTS_EVENTS" ]]; then
      in_list "$EVENT" "$TTS_EVENTS" && WANT_TTS=true
    else
      WANT_TTS=true
    fi
  fi

  if $WANT_TTS; then
    CMD="$CMD & say -v $TTS_VOICE \"$TTS_TEXT\" 2>/dev/null"
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
# Auto-generated by configure-hooks.sh
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

  # Event-specific body
  if [[ "$EVENT" == "Stop" ]]; then
    # Stop: show success
    cat >> "$HOOK_SCRIPT" << HOOKEOF
(
  python3 $TIVOO_PY preset success --loop 3$LOAD_FLAG 2>/dev/null
) &
HOOKEOF
    if $WANT_TTS; then
      cat >> "$HOOK_SCRIPT" << HOOKEOF

say -v $TTS_VOICE "$TTS_TEXT" 2>/dev/null &
HOOKEOF
    fi

  elif [[ "$EVENT" == "Notification" ]]; then
    # Notification: read message from JSON input and speak it
    cat >> "$HOOK_SCRIPT" << HOOKEOF
(
  python3 $TIVOO_PY preset $PRESET --loop $LOOP$LOAD_FLAG 2>/dev/null
) &
HOOKEOF
    if $WANT_TTS; then
      cat >> "$HOOK_SCRIPT" << 'HOOKEOF'

# Extract notification message and speak it
MSG=$(echo "$INPUT" | jq -r '.message // .title // .text // empty' 2>/dev/null)
HOOKEOF
      cat >> "$HOOK_SCRIPT" << HOOKEOF
if [[ -n "\$MSG" ]]; then
  say -v $TTS_VOICE "$TTS_TEXT" 2>/dev/null
  say -v $TTS_VOICE "\$MSG" 2>/dev/null &
else
  say -v $TTS_VOICE "$TTS_TEXT" 2>/dev/null &
fi
HOOKEOF
    fi

  else
    # Standard: single preset + optional TTS
    cat >> "$HOOK_SCRIPT" << HOOKEOF
(
  $CMD
) &
HOOKEOF
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
  ls -1 "$HOOKS_DIR"/
  echo ""
  echo "=== Settings JSON ==="
  echo "$RESULT" | jq .
else
  echo "$RESULT" > "$SETTINGS_FILE"

  # Count enabled hooks
  COUNT=$(echo "$HOOKS_JSON" | jq 'length')
  echo "Configured $COUNT Tivoo hooks ($LANG) in $SETTINGS_FILE"
  echo "Hook scripts in $HOOKS_DIR/"
  echo ""
  echo "Enabled events:"
  echo "$HOOKS_JSON" | jq -r 'keys[]' | while read -r ev; do
    echo "  - $ev"
  done
fi
